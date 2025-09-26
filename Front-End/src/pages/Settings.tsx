import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import { useToast } from "@/hooks/use-toast"
import { 
  Settings as SettingsIcon, 
  Save, 
  RefreshCw,
  Eye,
  EyeOff,
  Github,
  Bot,
  Shield,
  AlertTriangle
} from "lucide-react"

interface SystemSettings {
  githubToken: string
  githubSecret: string
  repositoryName: string
  openaiApiKey: string
  webhookUrl: string
  autoProcessPRs: boolean
  enableLogging: boolean
  logLevel: string
}

const Settings = () => {
  const [settings, setSettings] = useState<SystemSettings>({
    githubToken: "",
    githubSecret: "",
    repositoryName: "",
    openaiApiKey: "",
    webhookUrl: "",
    autoProcessPRs: true,
    enableLogging: true,
    logLevel: "INFO",
    
  })
  
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [showTokens, setShowTokens] = useState({
    githubToken: false,
    githubSecret: false,
    openaiApiKey: false
  })
  const { toast } = useToast()
  const backendUrl = import.meta.env.VITE_BACK_END;
  const email = localStorage.getItem('user_email') || '';
  const password = localStorage.getItem('user_senha') || '';

  const access_token = localStorage.getItem("access_token")
  console.log('Token enviado:', access_token)
  const payload = { email, password }
  const params = new URLSearchParams({ email, password });

  const fetchSettings = async () => {
    try {
      setIsLoading(true)
      const response = await fetch(`${backendUrl}/api/settings?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
      });

      if (response.ok) {
        const data = await response.json()
        setSettings({
          ...data,
          // githubToken: data.githubToken ? `${data.githubToken.substring(0, 4)}...${data.githubToken.slice(-4)}` : "",
          // githubSecret: data.githubSecret ? `${data.githubSecret.substring(0, 4)}...${data.githubSecret.slice(-4)}` : "",
          // openaiApiKey: data.openaiApiKey ? `${data.openaiApiKey.substring(0, 7)}...${data.openaiApiKey.slice(-4)}` : ""
        })
      }
    } catch (error) {
      toast({
        title: "Erro",
        description: "Falha ao carregar configurações",
        variant: "destructive"
      })
    } finally {
      setIsLoading(false)
    }
  }

  const saveSettings = async () => {
    setIsSaving(true)
    const payload = { ...settings, email, password }
    try {
      const response = await fetch(`${backendUrl}/api/settings`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        toast({
          title: "Configurações Salvas",
          description: "As configurações foram atualizadas com sucesso. Reinicie o sistema para aplicar todas as mudanças.",
          variant: "default"
        })
      } else {
        throw new Error('Falha ao salvar')
      }
    } catch (error) {
      toast({
        title: "Erro",
        description: "Falha ao salvar configurações",
        variant: "destructive"
      })
    } finally {
      setIsSaving(false)
    }
  }

  const maskToken = (token: string, showFull: boolean) => {
    if (!token) return ""
    if (showFull) return token
    if (token.includes("...")) return token // Already masked
    return `${token.substring(0, 4)}...${token.slice(-4)}`
  }

  const toggleTokenVisibility = (tokenType: keyof typeof showTokens) => {
    setShowTokens(prev => ({
      ...prev,
      [tokenType]: !prev[tokenType]
    }))
  }

  const testConnection = async (service: "github" | "openai") => {
    try {
      const response = await fetch(`${backendUrl}/api/test-connection/${service}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        toast({
          title: `Conexão ${service === "github" ? "GitHub" : "OpenAI"} OK`,
          description: "Conexão testada com sucesso",
          variant: "default"
        })
      } else {
        throw new Error('Connection failed')
      }
    } catch (error) {
      toast({
        title: "Erro de Conexão",
        description: `Falha ao conectar com ${service === "github" ? "GitHub" : "OpenAI"}`,
        variant: "destructive"
      })
    }
  }

  useEffect(() => {
    fetchSettings()
  }, [])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Configurações</h1>
        <p className="text-muted-foreground">
          Gerencie as configurações do sistema de IA
        </p>
      </div>

      {/* Security Warning */}
      <Card className="bg-card shadow-card border-warning/20">
        <CardContent className="pt-6">
          <div className="flex items-start gap-3">
            <Shield className="h-5 w-5 text-warning mt-0.5" />
            <div>
              <h3 className="font-semibold text-warning">Configurações Sensíveis</h3>
              <p className="text-sm text-muted-foreground mt-1">
                Estas configurações contêm informações sensíveis. Certifique-se de que apenas administradores autorizados tenham acesso.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* GitHub Settings */}
      <Card className="bg-card shadow-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Github className="h-5 w-5" />
            Configurações do GitHub
          </CardTitle>
          <CardDescription>
            Configurações para integração com o GitHub
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="github-token">Token do GitHub</Label>
              <div className="flex gap-2">
                <Input
                  id="github-token"
                  type={showTokens.githubToken ? "text" : "password"}
                  value={maskToken(settings.githubToken, showTokens.githubToken)}
                  onChange={(e) => setSettings(prev => ({ ...prev, githubToken: e.target.value }))}
                  placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
                />
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => toggleTokenVisibility('githubToken')}
                >
                  {showTokens.githubToken ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </Button>
              </div>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="github-secret">GitHub Webhook Secret</Label>
              <div className="flex gap-2">
                <Input
                  id="github-secret"
                  type={showTokens.githubSecret ? "text" : "password"}
                  value={maskToken(settings.githubSecret, showTokens.githubSecret)}
                  onChange={(e) => setSettings(prev => ({ ...prev, githubSecret: e.target.value }))}
                  placeholder="webhook_secret_here"
                />
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => toggleTokenVisibility('githubSecret')}
                >
                  {showTokens.githubSecret ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </Button>
              </div>
            </div>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="repo-name">Nome do Repositório</Label>
            <Input
              id="repo-name"
              value={settings.repositoryName}
              onChange={(e) => setSettings(prev => ({ ...prev, repositoryName: e.target.value }))}
              placeholder="usuario/nome-do-repositorio"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="webhook-url">URL do Webhook</Label>
            <Input
              id="webhook-url"
              value={settings.webhookUrl}
              onChange={(e) => setSettings(prev => ({ ...prev, webhookUrl: e.target.value }))}
              placeholder="https://seu-dominio.com/webhook"
            />
          </div>

          <Button onClick={() => testConnection("github")} variant="outline">
            <Github className="h-4 w-4 mr-2" />
            Testar Conexão GitHub
          </Button>
        </CardContent>
      </Card>

      {/* AI Settings */}
      <Card className="bg-card shadow-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-5 w-5" />
            Configurações da IA
          </CardTitle>
          <CardDescription>
            Configurações para serviços de IA
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="openai-key">Chave da API OpenAI</Label>
            <div className="flex gap-2">
              <Input
                id="openai-key"
                type={showTokens.openaiApiKey ? "text" : "password"}
                value={maskToken(settings.openaiApiKey, showTokens.openaiApiKey)}
                onChange={(e) => setSettings(prev => ({ ...prev, openaiApiKey: e.target.value }))}
                placeholder="sk-xxxxxxxxxxxxxxxxxxxx"
              />
              <Button
                variant="outline"
                size="icon"
                onClick={() => toggleTokenVisibility('openaiApiKey')}
              >
                {showTokens.openaiApiKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </Button>
            </div>
          </div>

          <Button onClick={() => testConnection("openai")} variant="outline">
            <Bot className="h-4 w-4 mr-2" />
            Testar Conexão OpenAI
          </Button>
        </CardContent>
      </Card>

      {/* System Settings */}
      <Card className="bg-card shadow-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <SettingsIcon className="h-5 w-5" />
            Configurações do Sistema
          </CardTitle>
          <CardDescription>
            Configurações gerais do sistema
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Processar PRs Automaticamente</Label>
              <p className="text-sm text-muted-foreground">
                Processar novos PRs automaticamente quando recebidos via webhook
              </p>
            </div>
            <Switch
              checked={settings.autoProcessPRs}
              onCheckedChange={(checked) => setSettings(prev => ({ ...prev, autoProcessPRs: checked }))}
            />
          </div>

          <Separator />

          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Habilitar Logging</Label>
              <p className="text-sm text-muted-foreground">
                Registrar ações do sistema em logs
              </p>
            </div>
            <Switch
              checked={settings.enableLogging}
              onCheckedChange={(checked) => setSettings(prev => ({ ...prev, enableLogging: checked }))}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="log-level">Nível de Log</Label>
            <select
              id="log-level"
              value={settings.logLevel}
              onChange={(e) => setSettings(prev => ({ ...prev, logLevel: e.target.value }))}
              className="w-full px-3 py-2 border border-input bg-background rounded-md"
            >
              <option value="DEBUG">DEBUG</option>
              <option value="INFO">INFO</option>
              <option value="WARNING">WARNING</option>
              <option value="ERROR">ERROR</option>
            </select>
          </div>
        </CardContent>
      </Card>

      {/* Save Settings */}
      <Card className="bg-card shadow-card border-border">
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-warning" />
              <span className="text-sm text-muted-foreground">
                Algumas mudanças requerem reinicialização do sistema
              </span>
            </div>
            <div className="flex gap-2">
              <Button 
                onClick={fetchSettings}
                variant="outline"
                disabled={isLoading}
              >
                <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                Recarregar
              </Button>
              <Button 
                onClick={saveSettings}
                disabled={isSaving}
                variant="ai"
              >
                {isSaving ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    Salvando...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4 mr-2" />
                    Salvar Configurações
                  </>
                )}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Settings