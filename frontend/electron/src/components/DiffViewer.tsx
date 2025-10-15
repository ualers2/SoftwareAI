import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { FileCode, Plus, Minus } from "lucide-react";

interface DiffViewerProps {
  diff: string;
  modifiedFiles: string[];
  linesChanged: number;
}

export const DiffViewer = ({ diff, modifiedFiles, linesChanged }: DiffViewerProps) => {
  const formatDiffLine = (line: string) => {
    if (line.startsWith('+')) {
      return (
        <div className="flex items-start gap-2 text-success bg-success/5 px-3 py-1">
          <Plus className="w-4 h-4 mt-0.5 flex-shrink-0" />
          <span className="font-mono text-sm">{line.substring(1)}</span>
        </div>
      );
    }
    if (line.startsWith('-')) {
      return (
        <div className="flex items-start gap-2 text-destructive bg-destructive/5 px-3 py-1">
          <Minus className="w-4 h-4 mt-0.5 flex-shrink-0" />
          <span className="font-mono text-sm">{line.substring(1)}</span>
        </div>
      );
    }
    if (line.startsWith('@@')) {
      return (
        <div className="text-primary bg-primary/5 px-3 py-1 font-mono text-sm font-semibold">
          {line}
        </div>
      );
    }
    return (
      <div className="text-muted-foreground px-3 py-1 font-mono text-sm">
        {line}
      </div>
    );
  };

  return (
    <Card className="bg-card border-border shadow-card overflow-hidden">
      <div className="flex items-center justify-between p-4 border-b border-border bg-muted/30">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/10">
            <FileCode className="w-5 h-5 text-primary" />
          </div>
          <div>
            <h3 className="text-lg font-semibold">Changes</h3>
            <p className="text-sm text-muted-foreground">
              {modifiedFiles.length} files · {linesChanged} lines changed
            </p>
          </div>
        </div>
      </div>

      <div className="p-4 space-y-3">
        <div className="flex flex-wrap gap-2">
          {modifiedFiles.map((file, idx) => (
            <div 
              key={idx}
              className="px-3 py-1.5 rounded-md bg-muted border border-border text-sm font-mono"
            >
              {file}
            </div>
          ))}
        </div>

        <ScrollArea className="h-[400px] rounded-lg border border-border bg-muted/20">
          <div className="p-2">
            {diff.split('\n').map((line, idx) => (
              <div key={idx}>
                {formatDiffLine(line)}
              </div>
            ))}
          </div>
        </ScrollArea>
      </div>
    </Card>
  );
};
