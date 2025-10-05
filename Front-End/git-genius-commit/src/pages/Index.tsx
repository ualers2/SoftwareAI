// src\pages\Index.tsx
import { useState, useEffect, useCallback } from "react";
import { GitConfig } from "@/types/git";
import { RepositorySelector } from "@/components/RepositorySelector";
import { ConfigPanel } from "@/components/ConfigPanel";
import { StatusMonitor } from "@/components/StatusMonitor";
import { DiffViewer } from "@/components/DiffViewer";
import { CommitPreview } from "@/components/CommitPreview";
import { useGitOperations } from "@/hooks/useGitOperations";
import { toast } from "sonner";
import { GitBranch } from "lucide-react";

const Index = () => {
  const [repoPath, setRepoPath] = useState<string>("");
  const [config, setConfig] = useState<GitConfig>();
  const [gitDiff, setGitDiff] = useState<string>(""); // Estado para armazenar o diff

  const {
    status,
    commitMessage,
    isAnalyzing,
    isCommitting,
    toggleMonitoring, 
    refreshStatus,
    analyzeChanges, 
    executeCommit,
    fetchAndCombineStatus,
  } = useGitOperations();

  const fetchDiff = useCallback(async (path: string) => {
    if (!path) {
      setGitDiff("");
      return;
    }
    try {
      // Nota: Esta função de IPC precisa ser adicionada ao seu useGitOperations.ts e preload.cjs, se ainda não estiver lá!
      const diff = await window.electronAPI.git.getDiff(path); 
      setGitDiff(diff);
    } catch (error) {
      console.error("Failed to fetch git diff:", error);
      setGitDiff("Error loading diff.");
    }
  }, []);

  // Efeito para atualizar o diff sempre que houver mudança de repo ou status
  useEffect(() => {
    if (repoPath && status.has_changes) {
      fetchDiff(repoPath);
    } else if (repoPath && !status.has_changes) {
      setGitDiff("No pending changes to display.");
    } else {
        setGitDiff("");
    }
  }, [repoPath, status.has_changes, fetchDiff]);


  // 1. Função de seleção de repositório
  const handleRepoSelect = (path: string) => {
    setRepoPath(path);
    toast.success("Repository selected");
    fetchAndCombineStatus(path); 
    fetchDiff(path);
  };
  
  // 2. Função para salvar a configuração
  const handleConfigSave = (newConfig: GitConfig) => {
    setConfig(newConfig);
    toast.success("Configuration saved");
  };

  // 3. Função para análise manual
  const handleAnalyze = async () => {
    if (!repoPath) {
      toast.error("Please select a repository first.");
      return;
    }
    if (!status.has_changes) {
        toast.info("No changes detected to analyze.");
        return;
    }
    // Chama a função do hook useGitOperations
    await analyzeChanges(repoPath, config);
  }

  // 4. Função de commit
  const handleCommit = async () => {
    if (!commitMessage || !repoPath) return;
    await executeCommit(repoPath, commitMessage.commit_message, config.auto_push);
  };
  
  // 5. Conecta o toggle ao hook
  const handleToggleMonitoring = () => {
      if (!repoPath) {
        toast.error("Select a repository path first to start monitoring.");
        return;
      }
      toggleMonitoring(repoPath, config);
  }


  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50 sticky top-0 z-50 bg-background/80 backdrop-blur-xl">
        <div className="container mx-auto px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <GitBranch className="w-5 h-5 text-foreground" />
              <h1 className="text-xl font-medium tracking-tight text-foreground">
                Git Context Layer
              </h1>
            </div>
            <p className="text-sm text-muted-foreground hidden md:block">
              AI-Powered Commit Management
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {/* Left Column - Config & Status */}
          <div className="lg:col-span-1 space-y-8">
            <RepositorySelector
              onSelect={handleRepoSelect}
              currentPath={repoPath}
            />
            
            <StatusMonitor
              status={status}
              onToggleMonitoring={handleToggleMonitoring} 
              onRefresh={() => repoPath && refreshStatus(repoPath)} 
            />

          </div>

          {/* Right Column - Diff & Commit */}
          <div className="lg:col-span-2 space-y-8">
            <DiffViewer
              // AGORA USANDO O ESTADO REAL
              diff={gitDiff} 
              modifiedFiles={status.modified_files}
              linesChanged={status.lines_changed}
            />

            <CommitPreview
              message={commitMessage?.commit_message || ""}
              status={commitMessage?.status || 'NO_CHANGES'}
              onCommit={handleCommit}
              onAnalyze={handleAnalyze} // NOVO: Conecta o botão de análise manual
              isLoading={isCommitting || isAnalyzing} // Considera ambos os estados de loading
            />

            <ConfigPanel
              config={config}
              onSave={handleConfigSave}
            />

          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;