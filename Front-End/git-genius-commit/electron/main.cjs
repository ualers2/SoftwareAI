// electron/main.cjs
const { app, BrowserWindow, ipcMain, dialog } = require("electron");
const path = require("path");
const { spawn } = require("child_process");
// adicione no topo do arquivo, logo após imports
let mainWindow = null;
let nodeCrypto = null;
try {
  nodeCrypto = require('crypto');
} catch (e) {
  nodeCrypto = null;
}
// Estado global do monitoramento
const monitoringState = {
  isMonitoring: false,
  lastActivityTime: Date.now(),
  checkInterval: null,
  currentRepoPath: null,
  inFlight: false,               // evita chamadas concorrentes
  lastPayloadHash: null,         // hash do último diff+files enviado
  lastAnalysisTimestamp: 0,      // quando foi a ultima análise
  throttle_ms: 60 * 1000,        // evita re-enviar mesmo payload por 60s (configurável)
  config: {
    lines_threshold: 10,
    files_threshold: 1,
    time_threshold: 30,
    auto_push: false,
    require_tests: false,
    api_endpoint: "https://your-vps.com/analyze_and_commit",
    api_key: "",
  },
};


const backend = 'http://localhost:5910'
const accessToken = "t7gwqwkNVXRFkto97ISidO96y68CSyRMGgwcwy_Qgr0"

/**
 * computeHash - retorna um hash hex (sha256 preferencialmente) para a string dada.
 * Tenta: Node crypto -> Web Crypto (subtle) -> fallback FNV-1a.
 * Retorna Promise<string>.
 */
async function computeHash(str) {
  // 1) Node createHash
  if (nodeCrypto && typeof nodeCrypto.createHash === 'function') {
    try {
      return nodeCrypto.createHash('sha256').update(str).digest('hex');
    } catch (e) {
      console.warn("[hash] node createHash failed, falling back:", e && e.message);
    }
  }

  // 2) Web Crypto (async)
  if (typeof globalThis !== "undefined" && globalThis.crypto && crypto.subtle && typeof crypto.subtle.digest === 'function') {
    try {
      const encoder = new TextEncoder();
      const data = encoder.encode(str);
      const hashBuffer = await crypto.subtle.digest('SHA-256', data);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    } catch (e) {
      console.warn("[hash] web subtle.digest failed, falling back:", e && e.message);
    }
  }

  // 3) Fallback determinístico (FNV-1a) — não criptográfico, mas suficiente para dedupe
  let h = 2166136261 >>> 0;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  // retorna hex com padding
  return (h >>> 0).toString(16).padStart(8, '0');
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  if (process.env.NODE_ENV === "development") {
    win.loadURL("http://localhost:4343");
    win.webContents.openDevTools();
  } else {
    win.loadFile(path.join(__dirname, "..", "dist", "index.html"));
  }

  return win;
}

function runGitCommand(repoPath, ...args) {
  return new Promise((resolve, reject) => {
    console.log(`[git] running: git ${args.join(' ')} -C ${repoPath}`);
    const git = spawn("git", ["-C", repoPath, ...args], { windowsHide: true });
    let stdout = "";
    let stderr = "";

    git.stdout.on("data", (data) => { stdout += data.toString(); });
    git.stderr.on("data", (data) => { stderr += data.toString(); });

    git.on("error", (err) => {
      // erro em spawn (ex: git não encontrado)
      reject(new Error(`Failed to spawn git: ${err.message}`));
    });

    git.on("close", (code) => {
      if (code === 0) {
        resolve(stdout.trim());
      } else {
        // anexa stdout+stderr para debug
        const msg = stderr.trim() || stdout.trim() || `Git command failed with code ${code}`;
        reject(new Error(msg));
      }
    });
  });
}
async function ensureGitUserConfigured(repoPath) {
  try {
    const name = (await runGitCommand(repoPath, "config", "--get", "user.name")).trim();
    const email = (await runGitCommand(repoPath, "config", "--get", "user.email")).trim();
    if (name && email) return { ok: true };

    // Se faltar qualquer um, tenta definir localmente (não sobrescreve global).
    const fallbackName = process.env.GIT_AUTHOR_NAME || "Git Context Layer";
    const fallbackEmail = process.env.GIT_AUTHOR_EMAIL || "no-reply@git-context.local";

    if (!name) await runGitCommand(repoPath, "config", "user.name", fallbackName);
    if (!email) await runGitCommand(repoPath, "config", "user.email", fallbackEmail);

    console.warn(`[git] set local user.name/user.email => ${fallbackName} <${fallbackEmail}>`);
    return { ok: true, set: true };
  } catch (err) {
    // se falhar ao checar, apenas retorna false para o chamador lidar
    return { ok: false, error: err.message || String(err) };
  }
}


// Analisa o status do Git
async function getGitStatus(repoPath) {
  try {
    // 1. Status básico para modified files
    const porcelain = await runGitCommand(repoPath, "status", "--porcelain");
    const files = porcelain
      .split("\n")
      .filter((line) => line.trim())
      .map((line) => line.substring(3).trim()); // trim no nome do arquivo

    // 2. Diff para lines changed
    const numstat = await runGitCommand(repoPath, "diff", "--numstat");
    let linesChanged = 0;

    numstat.split("\n").forEach((line) => {
      if (line.trim()) {
        const parts = line.split("\t");
        if (parts.length >= 3) {
          const [insertions, deletions] = parts;
          if (!isNaN(parseInt(insertions))) linesChanged += parseInt(insertions);
          if (!isNaN(parseInt(deletions))) linesChanged += parseInt(deletions);
        }
      }
    });

    return {
      modified_files: files,
      lines_changed: linesChanged,
      has_changes: files.length > 0,
    };
  } catch (error) {
    console.error("Error getting git status:", error.message);
    // Rejeita a promise para que o frontend possa exibir o erro
    throw new Error(error.message); 
  }
}

// Obtém o diff completo
async function getGitDiff(repoPath) {
  try {
    // Usamos git diff para as mudanças não staged
    return await runGitCommand(repoPath, "diff"); 
  } catch (error) {
    console.error("Error getting git diff:", error.message);
    throw new Error(error.message);
  }
}

// Executa commit
async function executeCommit(repoPath, message, autoPush = false) {
  try {
    // 0) garante que há mudanças
    const status = await getGitStatus(repoPath);
    if (!status.has_changes) {
      throw new Error("No changes to commit.");
    }

    // 1) adiciona tudo
    await runGitCommand(repoPath, "add", ".");

    // 2) tenta commit; se falhar por user config, tenta fixar e re-commit uma vez
    try {
      await runGitCommand(repoPath, "commit", "-m", message);
    } catch (commitErr) {
      const errMsg = commitErr.message || String(commitErr);
      // detecta erro clássico do Git sobre identidade do usuário
      if (errMsg.includes("Please tell me who you are") || errMsg.includes("user.name")) {
        const ensure = await ensureGitUserConfigured(repoPath);
        if (ensure.ok) {
          // tenta novo commit uma vez
          await runGitCommand(repoPath, "commit", "-m", message);
        } else {
          throw new Error(`Commit failed and couldn't configure git user: ${ensure.error || 'unknown'}`);
        }
      } else {
        // mantém erro original para debug
        throw commitErr;
      }
    }

    if (autoPush) {
      await runGitCommand(repoPath, "push");
    }
    return { success: true };
  } catch (error) {
    console.error("Error executing commit:", error.message || error);
    throw error;
  }
}


// Verifica se deve disparar análise (Lógica de Monitoramento)
async function shouldTrigger(repoPath, config) {
  const status = await getGitStatus(repoPath);

  if (!status.has_changes) {
    monitoringState.lastActivityTime = Date.now();
    return { shouldTrigger: false, status };
  }

  if (
    status.modified_files.length < config.files_threshold ||
    status.lines_changed < config.lines_threshold
  ) {
    return { shouldTrigger: false, status };
  }

  const timeSinceLastActivity =
    (Date.now() - monitoringState.lastActivityTime) / 1000;

  if (timeSinceLastActivity < config.time_threshold) {
    return { shouldTrigger: false, status };
  }

  return { shouldTrigger: true, status };
}

async function analyzeAndCommit(repoPath, config, mainWindow) {
  // Proteção: evita concorrência
  if (monitoringState.inFlight) {
    console.log("[monitor] Analysis already in-flight — skipping new analyzeAndCommit call");
    return;
  }

  // marca que estamos rodando
  monitoringState.inFlight = true;

  try {
    const status = await getGitStatus(repoPath);
    const diff = await getGitDiff(repoPath);

    // calcula hash do payload (diff + lista de arquivos) para deduplicação
    const payload = { diff, files: status.modified_files };
    const payloadHash = await computeHash(JSON.stringify(payload));
    
    // se o mesmo payload foi enviado recentemente, respeita throttle_ms
    const now = Date.now();
    if (monitoringState.lastPayloadHash === payloadHash &&
        (now - monitoringState.lastAnalysisTimestamp) < monitoringState.throttle_ms) {
      console.log("[monitor] Duplicate payload within throttle window — skipping analysis");
      return;
    }

    // indica ao frontend que estamos analisando
    mainWindow?.webContents.send("git:analyzing", { status });

    // chama endpoint remoto
    const response = await fetch(`${backend}/api/prai/diff_context`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-TOKEN": `${accessToken}`,
      },
      body: JSON.stringify({
        diff: diff,
        files: status.modified_files,
        model: config.ai_model || "gpt-5-nano",
      }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} - ${response.statusText}`);
    }

    const result = await response.json();
    const commitMessage = `${result.commit_message}`;

    // envia mensagem gerada ao frontend
    mainWindow?.webContents.send("git:commitGenerated", {
      commit_message: commitMessage,
      status: "READY",
    });

    // realiza commit automático se configurado
    if (config.auto_commit !== false) {
      await executeCommit(repoPath, commitMessage, config.auto_push);
      mainWindow?.webContents.send("git:committed", { success: true });
    }

    // atualiza registro de payload/análise
    monitoringState.lastPayloadHash = payloadHash;
    monitoringState.lastAnalysisTimestamp = Date.now();
    monitoringState.lastActivityTime = Date.now();
  } catch (error) {
    console.error("Error analyzing and committing:", error.message || error);
    mainWindow?.webContents.send("git:error", {
      error: error.message || String(error),
    });
  } finally {
    // desbloqueia para próximas análises (sempre)
    monitoringState.inFlight = false;
  }
}


// Inicia monitoramento (Lógica de Monitoramento)
function startMonitoring(repoPath, config, mainWindow) {
  if (monitoringState.isMonitoring) {
    stopMonitoring();
  }

  monitoringState.isMonitoring = true;
  monitoringState.currentRepoPath = repoPath;
  monitoringState.config = config;
  monitoringState.lastActivityTime = Date.now();

  // Verifica imediatamente se há mudanças pendentes
  shouldTrigger(repoPath, config)
    .then(({ shouldTrigger: trigger, status }) => {
      mainWindow?.webContents.send("git:statusUpdate", status);

      if (trigger) {
        if (!monitoringState.inFlight) {
          analyzeAndCommit(repoPath, config, mainWindow);
        } else {
          console.log("[monitor] initial trigger but analysis already in-flight");
        }
      }
    })

  // Inicia verificação periódica
  monitoringState.checkInterval = setInterval(async () => {
    try {
      // evita novas verificações se já estivermos analisando
      if (monitoringState.inFlight) {
        console.log("[monitor] skipping periodic check because analysis is in-flight");
        return;
      }

      const { shouldTrigger: trigger, status } = await shouldTrigger(repoPath, config);

      mainWindow?.webContents.send("git:statusUpdate", status);

      if (trigger) {
        // dupla proteção: checa inFlight e dedupe internamente em analyzeAndCommit também
        await analyzeAndCommit(repoPath, config, mainWindow);
      }
    } catch (error) {
      mainWindow?.webContents.send("git:error", { error: error.message });
      stopMonitoring();
    }
  }, 5000); // Verifica a cada 5 segundos

  console.log("🚀 Git Context Layer monitoring started");
}

// Para monitoramento (Lógica de Monitoramento)
function stopMonitoring() {
  // ... (Lógica de stopMonitoring mantida)
  if (monitoringState.checkInterval) {
    clearInterval(monitoringState.checkInterval);
    monitoringState.checkInterval = null;
  }
  monitoringState.isMonitoring = false;
  monitoringState.currentRepoPath = null;
  console.log("⏹️  Git Context Layer monitoring stopped");
}


app.whenReady().then(() => {
  // 1) Registra todos os IPC handlers ANTES de carregar o renderer
  ipcMain.handle("dialog:selectFolder", async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      properties: ["openDirectory"],
    });
    if (canceled) return null;
    return filePaths[0];
  });

  ipcMain.handle("git:getStatus", async (event, repoPath) => {
    return await getGitStatus(repoPath);
  });

  ipcMain.handle("git:getMonitoringState", () => {
    return {
      is_monitoring: monitoringState.isMonitoring,
    };
  });

  ipcMain.handle("git:getDiff", async (event, repoPath) => {
    return await getGitDiff(repoPath);
  });

  ipcMain.handle("git:analyze", async (event, { repoPath, config }) => {
    try {
      const status = await getGitStatus(repoPath);
      const diff = await getGitDiff(repoPath);
      const response = await fetch(config.api_endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-TOKEN": `${config.api_key}`,
        },
        body: JSON.stringify({
          diff: diff,
          files: status.modified_files,
          model: config.ai_model || "gpt-5-nano",
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const result = await response.json();
      return {
        commit_message: `${result.subject}\n\n${result.body}`,
        status: "READY",
      };
    } catch (error) {
      console.error("Error analyzing:", error);
      throw error;
    }
  });

  ipcMain.handle("git:commit", async (event, { repoPath, message, autoPush }) => {
    return await executeCommit(repoPath, message, autoPush);
  });

  ipcMain.handle("git:toggleMonitoring", async (event, { repoPath, config }) => {
    if (monitoringState.isMonitoring && monitoringState.currentRepoPath === repoPath) {
      stopMonitoring();
      return { is_monitoring: false };
    } else {
      // Inicia e o startMonitoring usa mainWindow (que já vamos setar abaixo)
      startMonitoring(repoPath, config, mainWindow);
      return { is_monitoring: true };
    }
  });

  // 2) Agora criamos a janela e só então carregamos o renderer
  mainWindow = createWindow();

  if (process.env.NODE_ENV === "development") {
    mainWindow.loadURL("http://localhost:4343");
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, "..", "dist", "index.html"));
  }

});
app.on("window-all-closed", () => {
  stopMonitoring();
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});