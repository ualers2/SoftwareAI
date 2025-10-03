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

  const accessToken = "t7gwqwkNVXRFkto97ISidO96y68CSyRMGgwcwy_Qgr0"
  const email = "freitasalexandre810@gmail.com"
  const password = "teste"

  // Carrega config do backend
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
          api_key: data.openaiApiKey || "",
          api_endpoint: data.webhookUrl || "",
          ai_model: "gpt-5-mini", // default se backend não retorna
          lines_threshold: 50,
          files_threshold: 5,
          time_threshold: 60,
          auto_push: data.autoProcessPRs || false,
          require_tests: data.enableLogging || false,
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
          githubToken: "", // se precisar mandar, pode mapear
          githubSecret: "",
          repositoryName: "",
          openaiApiKey: localConfig.api_key,
          webhookUrl: localConfig.api_endpoint,
          autoProcessPRs: localConfig.auto_push,
          enableLogging: localConfig.require_tests,
          logLevel: "INFO",
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
          <Label htmlFor="api-key" className="text-sm font-medium">API Key</Label>
          <Input
            id="api-key"
            type="password"
            value={localConfig.api_key}
            onChange={(e) => setLocalConfig({ ...localConfig, api_key: e.target.value })}
            className="font-mono text-sm bg-input border-border"
          />
        </div>

        <div className="space-y-3">
          <Label htmlFor="api-endpoint" className="text-sm font-medium">API Endpoint</Label>
          <Input
            id="api-endpoint"
            type="text"
            value={localConfig.api_endpoint}
            onChange={(e) => setLocalConfig({ ...localConfig, api_endpoint: e.target.value })}
            className="font-mono text-sm bg-input border-border"
          />
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
          <Label htmlFor="require-tests">Require Tests</Label>
          <Switch
            id="require-tests"
            checked={localConfig.require_tests}
            onCheckedChange={(checked) => setLocalConfig({ ...localConfig, require_tests: checked })}
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
