// src/hooks/useGitOperations.ts
import { useState, useEffect, useCallback } from "react";
import { GitStatus, GitConfig, CommitMessage } from "@/types/git";
import { toast } from "sonner";

const INITIAL_STATUS: GitStatus = {
  modified_files: [],
  lines_changed: 0,
  has_changes: false,
  last_check: new Date(0), 
  is_monitoring: false,
};

declare global {
  interface Window {
    electronAPI: {
      git: {
        
        getStatus: (repoPath: string) => Promise<Omit<GitStatus, 'last_check' | 'is_monitoring'>>;
        getMonitoringState: () => Promise<{ is_monitoring: boolean }>;
        toggleMonitoring: (repoPath: string, config: GitConfig) => Promise<{ is_monitoring: boolean }>;
        onStatusUpdate: (callback: (status: Omit<GitStatus, 'last_check' | 'is_monitoring'>) => void) => void;
        onAnalyzing: (callback: (data: { status: any }) => void) => void;
        onCommitGenerated: (callback: (data: CommitMessage) => void) => void;
        onCommitted: (callback: (data: { success: boolean }) => void) => void;
        onError: (callback: (data: { error: string }) => void) => void;
        analyze: (repoPath: string, config: GitConfig) => Promise<CommitMessage>;
        commit: (repoPath: string, message: string, autoPush: boolean) => Promise<{ success: boolean }>;
        getDiff: (repoPath: string) => Promise<string>; // Adicionado para uso no Index.tsx
      };
      sendToken: (token: string) => void; 
      sendEmail: (email: string) => void; 
      sendPassword: (password: string) => void; 
      selectFolder: () => Promise<string | null>;
    };
  }
}

export const useGitOperations = () => {
  const [status, setStatus] = useState<GitStatus>(INITIAL_STATUS);
  const [commitMessage, setCommitMessage] = useState<CommitMessage | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isCommitting, setIsCommitting] = useState(false);
  // Adicione um small helper de sleep
  const sleep = (ms: number) => new Promise(res => setTimeout(res, ms));

  const fetchAndCombineStatus = useCallback(async (repoPath: string) => {
    if (!repoPath) return;

    // Tentativa com retry específico para "No handler registered"
    const maxRetries = 3;
    let attempt = 0;
    while (attempt < maxRetries) {
      try {
        // Faz as duas chamadas de IPC em paralelo
        const [gitStatus, monitoringState] = await Promise.all([
          window.electronAPI.git.getStatus(repoPath),
          window.electronAPI.git.getMonitoringState(),
        ]);

        setStatus(prev => ({
          ...prev,
          ...gitStatus,
          ...monitoringState,
          last_check: new Date(),
        }));
        return;
      } catch (error: any) {
        const msg = error?.message || String(error);
        // Se for o erro conhecido, espera e retry — caso contrário propaga
        if (msg.includes("No handler registered") || msg.includes("No handler for")) {
          attempt++;
          console.warn(`git:getStatus handler not ready yet — retry ${attempt}/${maxRetries}`);
          // espera curta antes de tentar novamente
          await sleep(150 * attempt);
          continue;
        } else {
          console.error("Failed to fetch git status:", error);
          toast.error(`Error fetching Git status: ${msg}. Is the path a Git repository?`);
          throw error;
        }
      }
    }

    // Se sair do loop => falhou após retries
    toast.error("IPC handlers not ready (git:getStatus). Reinicie o app se o erro persistir.");
  }, []);


  const refreshStatus = useCallback((repoPath: string) => {
    fetchAndCombineStatus(repoPath);
  }, [fetchAndCombineStatus]);

  const toggleMonitoring = useCallback(async (repoPath: string, config: GitConfig) => {
    if (!repoPath) {
      toast.error("Select a repository path first.");
      return;
    }
    try {
      const result = await window.electronAPI.git.toggleMonitoring(repoPath, config);
      setStatus(prev => ({ ...prev, is_monitoring: result.is_monitoring }));

      if (result.is_monitoring) {
        toast.info("Monitoring started.");
        refreshStatus(repoPath); 
      } else {
        toast.info("Monitoring paused.");
      }
    } catch (error) {
      console.error("Failed to toggle monitoring:", error);
      toast.error("Error toggling monitoring.");
    }
  }, [refreshStatus]);


  const analyzeChanges = useCallback(async (repoPath: string, config: GitConfig) => {
    if (!repoPath || isAnalyzing) return;
    setIsAnalyzing(true);
    setCommitMessage(null);
    toast.info("Analyzing changes with AI...");
    try {
      const result = await window.electronAPI.git.analyze(repoPath, config);
      setCommitMessage(result);
      toast.success("Commit message generated!");
    } catch (error) {
      setCommitMessage({ commit_message: "", status: 'ERROR' });
      toast.error(`Analysis failed: ${error.message}. Check API endpoint and key.`);
    } finally {
      setIsAnalyzing(false);
    }
  }, [isAnalyzing]);
  
  
  const executeCommit = useCallback(async (repoPath: string, message: string, autoPush: boolean) => {
    if (!repoPath || isCommitting) return;
    setIsCommitting(true);
    toast.info("Committing changes...");
    try {
      await window.electronAPI.git.commit(repoPath, message, autoPush);
      toast.success(`Commit successful! ${autoPush ? 'And pushed!' : ''}`);
      setCommitMessage(null);
      refreshStatus(repoPath); 
    } catch (error) {
      toast.error(`Commit failed: ${error.message}`);
    } finally {
      setIsCommitting(false);
    }
  }, [isCommitting, refreshStatus]);

  useEffect(() => {
    window.electronAPI.git.onStatusUpdate((gitStatus) => {
      setStatus(prev => ({
        ...prev,
        ...gitStatus,
        is_monitoring: true,
        last_check: new Date(),
      }));
    });

    window.electronAPI.git.onCommitGenerated((data) => {
      setCommitMessage(data);
      setIsAnalyzing(false);
      toast.success("Auto-commit message generated.");
    });

    window.electronAPI.git.onAnalyzing(() => {
      setIsAnalyzing(true);
      toast.info("Auto-analyzing and processing changes...");
    });

    window.electronAPI.git.onCommitted(() => {
      toast.success("Auto-commit executed successfully.");
      setCommitMessage(null);
      setIsCommitting(false);
      // Não tentamos atualizar o status sem saber o repoPath correto
    });

    window.electronAPI.git.onError(({ error }) => {
      toast.error(`Monitoring Error: ${error}`);
      setIsAnalyzing(false);
      setIsCommitting(false);
    });

    // cleanup não estritamente necessário porque preload já removeAllListeners antes de adicionar,
    // mas colocar retorno é bom
    return () => {
      // Se quiser, pode remover listeners aqui via uma API de remoção específica
    };
  }, []);

  return {
    status,
    commitMessage,
    isAnalyzing,
    isCommitting,
    analyzeChanges,
    executeCommit,
    toggleMonitoring,
    refreshStatus,
    fetchAndCombineStatus,
  };
};