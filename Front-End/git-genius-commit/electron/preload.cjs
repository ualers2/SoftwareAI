// electron/preload.cjs 
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  selectFolder: () => ipcRenderer.invoke("dialog:selectFolder"),

  git: {
    getStatus: (repoPath) => ipcRenderer.invoke("git:getStatus", repoPath),
    getMonitoringState: () => ipcRenderer.invoke("git:getMonitoringState"),
    toggleMonitoring: (repoPath, config) => ipcRenderer.invoke("git:toggleMonitoring", { repoPath, config }),
    analyze: (repoPath, config) => ipcRenderer.invoke("git:analyze", { repoPath, config }),
    commit: (repoPath, message, autoPush) => ipcRenderer.invoke("git:commit", { repoPath, message, autoPush }),
    getDiff: (repoPath) => ipcRenderer.invoke("git:getDiff", repoPath),

    onStatusUpdate: (callback) => {
      ipcRenderer.removeAllListeners("git:statusUpdate");
      ipcRenderer.on("git:statusUpdate", (event, status) => callback(status));
    },
    onAnalyzing: (callback) => {
      ipcRenderer.removeAllListeners("git:analyzing");
      ipcRenderer.on("git:analyzing", (event, data) => callback(data));
    },
    onCommitGenerated: (callback) => {
      ipcRenderer.removeAllListeners("git:commitGenerated");
      ipcRenderer.on("git:commitGenerated", (event, data) => callback(data));
    },
    onCommitted: (callback) => {
      ipcRenderer.removeAllListeners("git:committed");
      ipcRenderer.on("git:committed", (event, data) => callback(data));
    },
    onError: (callback) => {
      ipcRenderer.removeAllListeners("git:error");
      ipcRenderer.on("git:error", (event, data) => callback(data));
    },
  }
});
