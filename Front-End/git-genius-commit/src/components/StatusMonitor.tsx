import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Activity, Play, Pause, RefreshCw } from "lucide-react";
import { GitStatus } from "@/types/git";

interface StatusMonitorProps {
  status: GitStatus;
  onToggleMonitoring: () => void;
  onRefresh: () => void;
}

export const StatusMonitor = ({ status, onToggleMonitoring, onRefresh }: StatusMonitorProps) => {
  return (
    <Card className="p-6 bg-card border-border shadow-card">
      <div className="flex items-center justify-between mb-6">
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
          {status.is_monitoring ? 'Active' : 'Paused'}
        </Badge>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="p-4 rounded-lg bg-muted/50 border border-border">
          <div className="text-sm text-muted-foreground mb-1">Modified Files</div>
          <div className="text-2xl font-bold text-primary">{status.modified_files.length}</div>
        </div>
        <div className="p-4 rounded-lg bg-muted/50 border border-border">
          <div className="text-sm text-muted-foreground mb-1">Lines Changed</div>
          <div className="text-2xl font-bold text-secondary">{status.lines_changed}</div>
        </div>
      </div>

      <div className="text-sm text-muted-foreground mb-4 font-mono">
        Last check: {status.last_check.toLocaleTimeString()}
      </div>

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
        <Button
          onClick={onRefresh}
          variant="outline"
          className="border-border hover:bg-muted"
        >
          <RefreshCw className="w-4 h-4" />
        </Button>
      </div>
    </Card>
  );
};
