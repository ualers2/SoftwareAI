// src\components\RepositorySelector.tsx
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { FolderGit2, Check } from "lucide-react";

interface RepositorySelectorProps {
  onSelect: (path: string) => void;
  currentPath?: string;
}

export const RepositorySelector = ({ onSelect, currentPath }: RepositorySelectorProps) => {
  const [path, setPath] = useState(currentPath || "");

  const handleSelect = async () => {
    const folderPath = await window.electronAPI.selectFolder();
    if (folderPath) {
      setPath(folderPath);
      onSelect(folderPath);
    }
  };

  return (
    <Card className="p-6 bg-card border-border shadow-card">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 rounded-lg bg-primary/10">
          <FolderGit2 className="w-5 h-5 text-primary" />
        </div>
        <h3 className="text-lg font-semibold">Repository Path</h3>
      </div>
      
      <div>
        <Button 
          onClick={handleSelect}
          className="bg-gradient-primary hover:shadow-glow transition-smooth flex items-center"
        >
          {path ? <Check className="w-4 h-4 mr-2" /> : null}
          Selecionar pasta
        </Button>

        {path && (
          <div className="mt-3 text-sm text-muted-foreground font-mono">
            Ativo: {path}
          </div>
        )}
      </div>
    </Card>
  );
};
