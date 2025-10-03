// electron/main.cjs
const { app, BrowserWindow, ipcMain, dialog } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

// Estado global do monitoramento
const monitoringState = {
  isMonitoring: false,
  lastActivityTime: Date.now(),
  checkInterval: null,
  currentRepoPath: null,
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
    const git = spawn("git", ["-C", repoPath, ...args]);
    let stdout = "";
    let stderr = "";

    git.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    git.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    git.on("close", (code) => {
      if (code === 0) {
        resolve(stdout.trim());
      } else {
        // Verifica se é um erro comum de "não é repo git"
        const gitError = stderr || `Git command failed with code ${code}`;
        if (gitError.includes('not a git repository')) {
          reject(new Error('The selected path is not a Git repository.'));
        } else {
          reject(new Error(gitError));
        }
      }
    });
  });
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
    await runGitCommand(repoPath, "add", ".");
    await runGitCommand(repoPath, "commit", "-m", message);

    if (autoPush) {
      await runGitCommand(repoPath, "push");
    }

    return { success: true };
  } catch (error) {
    console.error("Error executing commit:", error.message);
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

// Envia para API e processa commit (Lógica de Monitoramento)
async function analyzeAndCommit(repoPath, config, mainWindow) {
  try {
    const status = await getGitStatus(repoPath);
    const diff = await getGitDiff(repoPath);

    mainWindow.webContents.send("git:analyzing", { status });
    const response = await fetch(`${backend}/api/prai/gen`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        'X-API-TOKEN': `${accessToken}`,
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
    const commitMessage = `${result.subject}\n\n${result.body}`;

    mainWindow.webContents.send("git:commitGenerated", {
      commit_message: commitMessage,
      status: "READY",
    });

    if (config.auto_commit !== false) {
      await executeCommit(repoPath, commitMessage, config.auto_push);
      mainWindow.webContents.send("git:committed", { success: true });
    }

    monitoringState.lastActivityTime = Date.now();
  } catch (error) {
    console.error("Error analyzing and committing:", error.message);
    mainWindow.webContents.send("git:error", {
      error: error.message,
    });
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
      // usa optional chaining para evitar crash caso mainWindow ainda não esteja definido
      mainWindow?.webContents.send("git:statusUpdate", status);

      if (trigger) {
        analyzeAndCommit(repoPath, config, mainWindow);
      }
    })
    .catch(error => {
      // Trata erro no status inicial (ex: não é repo git)
      mainWindow?.webContents.send("git:error", { error: error.message });
      stopMonitoring();
    });

  // Inicia verificação periódica
  monitoringState.checkInterval = setInterval(async () => {
    try {
      // renomeia o campo desestruturado para evitar conflito com a função shouldTrigger
      const { shouldTrigger: trigger, status } = await shouldTrigger(repoPath, config);

      mainWindow?.webContents.send("git:statusUpdate", status);

      if (trigger) {
        analyzeAndCommit(repoPath, config, mainWindow);
      }
    } catch (error) {
      // Envia erro e para o monitoring se falhar periodicamente
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