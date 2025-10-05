import { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Settings, Save } from "lucide-react";
import { GitConfig } from "@/types/git";

export const ConfigPanel = () => {
  const [localConfig, setLocalConfig] = useState<GitConfig | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const backend = import.meta.env.VITE_BACK_END || ''

  const accessToken = localStorage.getItem('access_token') 
  const email = localStorage.getItem('user_email') 
  const password = localStorage.getItem('user_senha') 

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const res = await fetch(`${backend}/api/settings?email=${email}&password=${password}`, {
          
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-API-TOKEN': `${accessToken}`
          },
        });
        if (!res.ok) throw new Error("Erro ao carregar configurações");
        const data = await res.json();
        console.log("Config recebida:", data);

        setLocalConfig({
          ai_model: data.ai_model ?? 'gpt-5-nano',
          lines_threshold: data.linesThreshold ?? 50,
          files_threshold: data.filesThreshold ?? 5,
          time_threshold: data.timeThreshold ?? 60,
          throttle_ms: data.throttleMs ?? 60000,
          auto_push: data.autoPush ?? false,
          auto_commit: true,
          auto_create_pr: data.AutoCreatePr ?? false,
          GITHUB_TOKEN: data.GITHUB_TOKEN,
          commitLanguage: data.commitLanguage ?? 'en',
        });
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchSettings();
  }, []);

  const handleSave = async () => {
    if (!localConfig) return;
    setSaving(true);
    try {
      const res = await fetch(`${backend}/api/settings`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-API-TOKEN": accessToken,
        },
        body: JSON.stringify({

          ai_model: localConfig.ai_model,
          autoPush: localConfig.auto_push,
          AutoCreatePr: localConfig.auto_create_pr,
          linesThreshold: localConfig.lines_threshold,
          filesThreshold: localConfig.files_threshold,
          timeThreshold: localConfig.time_threshold,
          throttleMs: localConfig.throttle_ms,
          GITHUB_TOKEN: localConfig.GITHUB_TOKEN,
          commit_language: localConfig.commitLanguage,
        }),
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.error || "Erro ao salvar configurações");
      console.log("Config salva:", data);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  if (!localConfig) {
    return <div className="p-6">Carregando configurações...</div>;
  }

  return (
    <Card className="p-6 bg-card border-border shadow-card">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-secondary/10">
          <Settings className="w-5 h-5 text-secondary" />
        </div>
        <h3 className="text-lg font-semibold">Configuration</h3>
      </div>

      <div className="space-y-6">
        <div className="space-y-3">
          <Label htmlFor="api-key" className="text-sm font-medium">GitHub API Key</Label>
          <Input
            id="api-key"
            type="password"
            value={localConfig.GITHUB_TOKEN}
            onChange={(e) => setLocalConfig({ ...localConfig, GITHUB_TOKEN: e.target.value })}
            className="font-mono text-sm bg-input border-border"
          />
        </div>

        {/* <div className="space-y-3">
          <Label htmlFor="api-endpoint" className="text-sm font-medium">API Endpoint</Label>
          <Input
            id="api-endpoint"
            type="text"
            value={localConfig.api_endpoint}
            onChange={(e) => setLocalConfig({ ...localConfig, api_endpoint: e.target.value })}
            className="font-mono text-sm bg-input border-border"
          />
        </div> */}

        <div className="space-y-3">
          <Label htmlFor="ai-model" className="text-sm font-medium">Language</Label>
          <Select 
            value={localConfig.commitLanguage}
            onValueChange={(value) => setLocalConfig({ ...localConfig, commitLanguage: value })}
          >
            <SelectTrigger className="bg-input border-border">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="pt">Português</SelectItem>
              <SelectItem value="en">English</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-3">
          <Label htmlFor="ai-model" className="text-sm font-medium">AI Model</Label>
          <Select 
            value={localConfig.ai_model}
            onValueChange={(value) => setLocalConfig({ ...localConfig, ai_model: value })}
          >
            <SelectTrigger className="bg-input border-border">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="gpt-5-nano">GPT-5 Nano</SelectItem>
              <SelectItem value="gpt-5-mini">GPT-5 Mini</SelectItem>
              <SelectItem value="gpt-5">GPT-5</SelectItem>
              <SelectItem value="gpt-4">GPT-4</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Thresholds */}
        <div className="grid grid-cols-3 gap-4">
          <div className="space-y-2">
            <Label htmlFor="lines">Lines Threshold</Label>
            <Input
              id="lines"
              type="number"
              value={localConfig.lines_threshold}
              onChange={(e) => setLocalConfig({ ...localConfig, lines_threshold: parseInt(e.target.value) })}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="files">Files Threshold</Label>
            <Input
              id="files"
              type="number"
              value={localConfig.files_threshold}
              onChange={(e) => setLocalConfig({ ...localConfig, files_threshold: parseInt(e.target.value) })}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="time">Time Threshold (s)</Label>
            <Input
              id="time"
              type="number"
              value={localConfig.time_threshold}
              onChange={(e) => setLocalConfig({ ...localConfig, time_threshold: parseInt(e.target.value) })}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="time">Throttle (ms)</Label>
            <Input
              id="time"
              type="number"
              value={localConfig.throttle_ms}
              onChange={(e) => setLocalConfig({ ...localConfig, throttle_ms: parseInt(e.target.value) })}
            />
          </div>


        </div>

        {/* Switches */}
        <div className="flex items-center justify-between p-4 rounded-lg bg-muted/50 border border-border">
          <Label htmlFor="auto-push">Auto Push</Label>
          <Switch
            id="auto-push"
            checked={localConfig.auto_push}
            onCheckedChange={(checked) => setLocalConfig({ ...localConfig, auto_push: checked })}
          />
        </div>

        <div className="flex items-center justify-between p-4 rounded-lg bg-muted/50 border border-border">
          <Label htmlFor="require-tests">Auto Create Pr</Label>
          <Switch
            id="require-tests"
            checked={localConfig.auto_create_pr}
            onCheckedChange={(checked) => setLocalConfig({ ...localConfig, auto_create_pr: checked })}
          />
        </div>

        <Button 
          onClick={handleSave}
          disabled={saving}
          className="w-full bg-gradient-accent hover:shadow-accent transition-smooth"
        >
          <Save className="w-4 h-4 mr-2" />
          {saving ? "Saving..." : "Save Configuration"}
        </Button>
      </div>
    </Card>
  );
};
