// electron/main.cjs
const { app, BrowserWindow, ipcMain, dialog } = require("electron");
const path = require("path");
const { spawn } = require("child_process");
const simpleGit = require("simple-git");
// --- Safe fetch import (Node 18+, Electron) ---
let fetchFn;
try {
  // Node 18+ já tem fetch global
  if (typeof fetch !== "undefined") {
    fetchFn = fetch;
  } else {
    fetchFn = (...args) => import("node-fetch").then(({ default: f }) => f(...args));
  }
} catch {
  fetchFn = (...args) => import("node-fetch").then(({ default: f }) => f(...args));
}
global.fetch = fetchFn; // <-- injeta globalmente

let mainWindow = null;
let nodeCrypto = null;
let accessToken = null;
let user_email = null;
let user_senha = null;
try {
  nodeCrypto = require('crypto');
} catch (e) {
  nodeCrypto = null;
}
const monitoringState = {
  isMonitoring: false,
  lastActivityTime: Date.now(),
  checkInterval: null,
  currentRepoPath: null,
  inFlight: false,               
  lastPayloadHash: null,       
  lastAnalysisTimestamp: 0,      
  throttle_ms: 60 * 1000,        
  config: {
    lines_threshold: 10,
    files_threshold: 1,
    time_threshold: 30,
    auto_push: false,
    auto_create_pr: false,
    commitLanguage: "en",
    GITHUB_TOKEN: "none",
    api_endpoint: "https://your-vps.com/analyze_and_commit",
    api_key: "",
  },
};
const backend = 'http://localhost:5910'

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
async function loadBackendSettings() {
  try {
    const response = await fetch(`${backend}/api/settings?email=${user_email}&password=${user_senha}`, {
      headers: { "X-API-TOKEN": accessToken },
    });
    if (!response.ok) throw new Error(`Settings fetch failed: ${response.status}`);
    const data = await response.json();
    
    // aplica no monitoringState.config
    monitoringState.config = {
      ...monitoringState.config,
      lines_threshold: data.linesThreshold,
      files_threshold: data.filesThreshold,
      time_threshold: data.timeThreshold,
      auto_push: data.autoPush,
      auto_commit: true,
      auto_create_pr: data.AutoCreatePr,
      commitLanguage: data.commitLanguage,
      GITHUB_TOKEN: data.GITHUB_TOKEN,
      api_endpoint: `${backend}/api/prai/diff_context`,
    };

    console.log("⚙️ Loaded backend settings into monitoringState", monitoringState.config);
  } catch (err) {
    console.error("❌ Failed to load backend settings:", err);
  }
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
async function getGitDiff(repoPath) {
  try {
    // Usamos git diff para as mudanças não staged
    return await runGitCommand(repoPath, "diff"); 
  } catch (error) {
    console.error("Error getting git diff:", error.message);
    throw new Error(error.message);
  }
}
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
        // Detecta branch atual
        const branch = (await runGitCommand(repoPath, "rev-parse", "--abbrev-ref", "HEAD")).trim();

        try {
            await runGitCommand(repoPath, "push");
        } catch (pushErr) {
            const msg = pushErr.message || "";
            // se não há upstream configurado, define e tenta novamente
            if (msg.includes("no upstream branch")) {
                console.warn(`[git] Sem upstream, configurando: origin ${branch}`);
                await runGitCommand(repoPath, "push", "--set-upstream", "origin", branch);
            } else {
                throw pushErr;
            }
        }
    }
    return { success: true };
  } catch (error) {
    console.error("Error executing commit:", error.message || error);
    throw error;
  }
}
async function getGitCommitHash(repoPath) {
  try {
    // pega o hash do HEAD
    return await runGitCommand(repoPath, "rev-parse", "HEAD");
  } catch (error) {
    console.error("Error getting git commit hash:", error.message);
    return null;
  }
}
async function shouldTrigger(repoPath, config) {
  const cfg = normalizeConfig(config); // garante defaults
  const status = await getGitStatus(repoPath);

  if (!status.has_changes) {
    monitoringState.lastActivityTime = Date.now();
    return { shouldTrigger: false, status };
  }

  if (
    status.modified_files.length < cfg.files_threshold ||
    status.lines_changed < cfg.lines_threshold
  ) {
    return { shouldTrigger: false, status };
  }

  const timeSinceLastActivity =
    (Date.now() - monitoringState.lastActivityTime) / 1000;

  if (timeSinceLastActivity < cfg.time_threshold) {
    return { shouldTrigger: false, status };
  }

  return { shouldTrigger: true, status };
}


async function createPullRequest({ repoPath, title, body, config }) {
  const cfg = normalizeConfig(config);
  const git = simpleGit(repoPath);
  const currentBranch = (await git.revparse(["--abbrev-ref", "HEAD"])).trim();

  const remoteUrl = (await git.remote(["get-url", "origin"])).trim();
  const [_, owner, repo] = remoteUrl.match(/[:/]([^/]+)\/([^/.]+)(\.git)?$/) || [];

  if (!owner || !repo) throw new Error(`URL remota inválida: ${remoteUrl}`);

  const GITHUB_TOKEN = cfg.GITHUB_TOKEN;
  if (!GITHUB_TOKEN) throw new Error("GITHUB_TOKEN não configurado");

  const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/pulls`, {
    method: "POST",
    headers: {
      "Authorization": `token ${GITHUB_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title,
      head: currentBranch,
      base: "main",
      body,
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Erro ao criar PR: ${response.status} - ${text}`);
  }

  return await response.json();
}
async function analyzeAndCommit(repoPath, config, mainWindow) {
  // Proteção: evita concorrência
  if (monitoringState.inFlight) {
    console.log("[monitor] Analysis already in-flight — skipping new analyzeAndCommit call");
    return;
  }

  // marca que estamos rodando
  monitoringState.inFlight = true;

  (async () => {
    if (!user_email || !user_senha) {
    console.warn("⚠️ Email ou senha não definidos ainda. Ignorando loadBackendSettings.");
    return;
    }
    await loadBackendSettings();
  })();

  try {
    const cfg = normalizeConfig(config);
    const status = await getGitStatus(repoPath);
    const diff = await getGitDiff(repoPath);
    const commit_hash = await getGitCommitHash(repoPath);

    // calcula hash do payload (diff + lista de arquivos) para deduplicação
    const payload = { diff, files: status.modified_files, commit_hash };
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
    const response = await fetch(cfg.api_endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-TOKEN": `${accessToken}`,
      },
      body: JSON.stringify({
        diff: diff,
        files: status.modified_files,
        language: cfg.commitLanguage,
        hash: commit_hash,
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


    if (cfg.auto_commit) { // <--- usa cfg normalizado
      await executeCommit(repoPath, commitMessage, cfg.auto_push);
      mainWindow?.webContents.send("git:committed", { success: true });
    }

    
    if (cfg.auto_create_pr) {
        console.log(`[monitor] Auto-create PR ativo — criando pull request... `);

        try {
            const prResult = await createPullRequest({
                repoPath,
                title: commitMessage.split("\n")[0],
                body: `### Descrição\n${commitMessage}\n\n### Mudanças\n\`\`\`diff\n${diff.substring(0, 2000)}\n\`\`\``,
                config
            });
            mainWindow?.webContents.send("git:prCreated", prResult);
            console.log(`[monitor] PR criado com sucesso: ${prResult.html_url}`);
    } catch (err) {
            console.error("[monitor] Falha ao criar PR:", err);
            mainWindow?.webContents.send("git:prError", { error: err.message });
        }
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
function normalizeConfig(config = {}) {
  return {
    lines_threshold: config.lines_threshold ?? config.linesThreshold ?? monitoringState.config.lines_threshold,
    files_threshold: config.files_threshold ?? config.filesThreshold ?? monitoringState.config.files_threshold,
    time_threshold: config.time_threshold ?? config.timeThreshold ?? monitoringState.config.time_threshold,
    auto_push: config.auto_push ?? config.autoPush ?? monitoringState.config.auto_push,
    auto_create_pr: config.auto_create_pr ?? config.AutoCreatePr ?? monitoringState.config.auto_create_pr,
    api_endpoint: config.api_endpoint ?? config.apiEndpoint ?? monitoringState.config.api_endpoint,
    auto_commit: true,
    commitLanguage: config.commitLanguage ?? monitoringState.config.commitLanguage ?? 'en',
    GITHUB_TOKEN: config.GITHUB_TOKEN ?? monitoringState.config.GITHUB_TOKEN ?? 'none',
  };
}

function startMonitoring(repoPath, config, mainWindow) {
  if (monitoringState.isMonitoring) {
    stopMonitoring();
  }

  monitoringState.isMonitoring = true;
  monitoringState.currentRepoPath = repoPath;
  monitoringState.config = normalizeConfig(config);
  monitoringState.lastActivityTime = Date.now();

  shouldTrigger(repoPath, monitoringState.config)
    .then(({ shouldTrigger: trigger, status }) => {
      mainWindow?.webContents.send("git:statusUpdate", status);

      if (trigger) {
        if (!monitoringState.inFlight) {
          analyzeAndCommit(repoPath, monitoringState.config, mainWindow);
        } else {
          console.log("[monitor] initial trigger but analysis already in-flight");
        }
      }
    });

  // Inicia verificação periódica
  monitoringState.checkInterval = setInterval(async () => {
    try {
      // evita novas verificações se já estivermos analisando
      if (monitoringState.inFlight) {
        console.log("[monitor] skipping periodic check because analysis is in-flight");
        return;
      }

      const { shouldTrigger: trigger, status } = await shouldTrigger(repoPath, monitoringState.config);


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

app.whenReady().then(async () => {
  
  // 1) Registra todos os IPC handlers ANTES de carregar o renderer

  ipcMain.on("set-token", (event, token) => {
    accessToken = token;
    console.log("🔑 Token recebido no main:", accessToken);

    (async () => {
        if (!user_email || !user_senha) {
        console.warn("⚠️ Email ou senha não definidos ainda. Ignorando loadBackendSettings.");
        return;
        }
        await loadBackendSettings();
    })();
    });

  ipcMain.on("set-email", (event, email) => {
    user_email = email;
    console.log("🔑 email recebido no main:", user_email);

    (async () => {
        if (!user_email || !user_senha) {
        console.warn("⚠️ Email ou senha não definidos ainda. Ignorando loadBackendSettings.");
        return;
        }
        await loadBackendSettings();
    })();
    });

  ipcMain.on("set-password", (event, password) => {
    user_senha = password;
    console.log("🔑 password recebido no main:", user_senha);

    (async () => {
        if (!user_email || !user_senha) {
        console.warn("⚠️ Email ou senha não definidos ainda. Ignorando loadBackendSettings.");
        return;
        }
        await loadBackendSettings();
    })();
    });


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
      const commit_hash = await getGitCommitHash(repoPath);
      const cfg = normalizeConfig(config);  
      const response = await fetch(config.api_endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-TOKEN": `${accessToken}`,
        },
        body: JSON.stringify({
          diff: diff,
          files: status.modified_files,
          language: cfg.commitLanguage,
          hash: commit_hash,
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
      startMonitoring(repoPath, monitoringState.confi, mainWindow);
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