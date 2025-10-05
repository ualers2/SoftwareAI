import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Activity, Play, Pause, RefreshCw, Zap } from "lucide-react";
import { GitStatus, TokenStatus } from "@/types/git";
import { useEffect, useState } from "react";

interface StatusMonitorProps {
  status: GitStatus;
  onToggleMonitoring: () => void;
  onRefresh: () => void;
}

export const StatusMonitor = ({ status, onToggleMonitoring, onRefresh }: StatusMonitorProps) => {
  const [tokens, setTokens] = useState<TokenStatus>({
    tokensUsed: 0,
    tokenLimit: 0,
    tokenPercentUsed: 0
  });

  const backendUrl = import.meta.env.VITE_BACK_END;
  const access_token = localStorage.getItem("access_token");

  const fetchTokens = async () => {
    if (!access_token) return;
    try {
      const response = await fetch(`${backendUrl}/api/dashboard-data`, {
        headers: {
          "Content-Type": "application/json",
          "X-API-TOKEN": access_token
        }
      });
      if (!response.ok) {
        console.error("Erro ao buscar tokens:", response.status);
        return;
      }
      const data = await response.json();
      setTokens({
        tokensUsed: data.stats.tokensUsed ?? 0,
        tokenLimit: data.stats.tokenLimit ?? 0,
        tokenPercentUsed: data.stats.tokenPercentUsed ?? 0
      });
    } catch (error) {
      console.error("Erro ao buscar tokens:", error);
    }
  };

  useEffect(() => {
    fetchTokens();
    const interval = setInterval(fetchTokens, 30000); // atualizar a cada 30s
    return () => clearInterval(interval);
  }, []);

  return (
    <Card className="p-6 bg-card border-border shadow-card space-y-6">
      {/* Monitoramento */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-accent/10">
            <Activity className="w-5 h-5 text-accent" />
          </div>
          <h3 className="text-lg font-semibold">Status Monitor</h3>
        </div>
        <Badge 
          variant={status.is_monitoring ? "default" : "secondary"}
          className={status.is_monitoring ? "bg-success" : ""}
        >
          {status.is_monitoring ? "Active" : "Paused"}
        </Badge>
      </div>

      {/* Informações de Git */}
      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 rounded-lg bg-muted/50 border border-border">
          <div className="text-sm text-muted-foreground mb-1">Modified Files</div>
          <div className="text-2xl font-bold text-primary">{status.modified_files.length}</div>
        </div>
        <div className="p-4 rounded-lg bg-muted/50 border border-border">
          <div className="text-sm text-muted-foreground mb-1">Lines Changed</div>
          <div className="text-2xl font-bold text-secondary">{status.lines_changed}</div>
        </div>
      </div>

      {/* Última verificação */}
      <div className="text-sm text-muted-foreground mb-4 font-mono">
        Last check: {status.last_check.toLocaleTimeString()}
      </div>

      {/* Tokens */}
      <div className="p-4 rounded-lg bg-muted/50 border border-border">
        <div className="flex items-center justify-between mb-1">
          <span className="text-sm text-muted-foreground">Tokens Consumidos</span>
          <Zap className="w-4 h-4 text-primary" />
        </div>
        <div className="text-2xl font-bold text-primary">
          {tokens.tokensUsed.toLocaleString()} / {tokens.tokenLimit.toLocaleString()}
        </div>
        <div className="text-xs text-muted-foreground">{tokens.tokenPercentUsed}% do plano usado</div>
      </div>

      {/* Ações */}
      <div className="flex gap-3">
        <Button
          onClick={onToggleMonitoring}
          className={status.is_monitoring 
            ? "flex-1 bg-destructive hover:bg-destructive/90" 
            : "flex-1 bg-gradient-accent hover:shadow-accent transition-smooth"
          }
        >
          {status.is_monitoring ? (
            <>
              <Pause className="w-4 h-4 mr-2" />
              Pause Monitoring
            </>
          ) : (
            <>
              <Play className="w-4 h-4 mr-2" />
              Start Monitoring
            </>
          )}
        </Button>
        <Button onClick={onRefresh} variant="outline" className="border-border hover:bg-muted">
          <RefreshCw className="w-4 h-4" />
        </Button>
      </div>
    </Card>
  );
};