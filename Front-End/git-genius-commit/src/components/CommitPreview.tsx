import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { GitCommit, Sparkles, Copy, Check } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

interface CommitPreviewProps {
  message: string;
  status: 'SUCCESS' | 'NO_CHANGES' | 'ERROR';
  onCommit: () => void;
  isLoading: boolean;
}

export const CommitPreview = ({ message, status, onCommit, isLoading }: CommitPreviewProps) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message);
    setCopied(true);
    toast.success("Message copied to clipboard");
    setTimeout(() => setCopied(false), 2000);
  };

  const getStatusColor = () => {
    switch (status) {
      case 'SUCCESS':
        return 'text-success';
      case 'NO_CHANGES':
        return 'text-warning';
      case 'ERROR':
        return 'text-destructive';
    }
  };

  return (
    <Card className="bg-card border-border shadow-card overflow-hidden">
      <div className="flex items-center justify-between p-4 border-b border-border bg-gradient-glow">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-secondary/10">
            <Sparkles className="w-5 h-5 text-secondary" />
          </div>
          <div>
            <h3 className="text-lg font-semibold">AI-Generated Commit</h3>
            <p className={`text-sm font-medium ${getStatusColor()}`}>
              Status: {status}
            </p>
          </div>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={handleCopy}
          disabled={!message}
          className="border-border hover:bg-muted"
        >
          {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
        </Button>
      </div>

      <div className="p-4">
        <ScrollArea className="h-[200px] rounded-lg border border-border bg-muted/20">
          <div className="p-4">
            {message ? (
              <pre className="text-sm font-mono whitespace-pre-wrap leading-relaxed">
                {message}
              </pre>
            ) : (
              <p className="text-muted-foreground text-sm text-center py-8">
                No commit message generated yet
              </p>
            )}
          </div>
        </ScrollArea>

        <Button
          onClick={onCommit}
          disabled={!message || isLoading || status !== 'SUCCESS'}
          className="w-full mt-4 bg-gradient-primary hover:shadow-glow transition-smooth"
        >
          <GitCommit className="w-4 h-4 mr-2" />
          {isLoading ? 'Committing...' : 'Commit & Push'}
        </Button>
      </div>
    </Card>
  );
};
