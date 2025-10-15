import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { 
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { useToast } from "@/hooks/use-toast"
import { 
  Zap, 
  GitPullRequest, 
  Rocket, 
  RefreshCw,
  Play,
  AlertTriangle,
  CheckCircle
} from "lucide-react"

const Controls = () => {
  const [prNumber, setPrNumber] = useState("")
  const [customPayload, setCustomPayload] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [isDeploying, setIsDeploying] = useState(false)
  const { toast } = useToast()
  const backendUrl = import.meta.env.VITE_BACK_END;

  const [rateLimits, setRateLimits] = useState<any>(null)   
  const [redoMerge, setRedoMerge] = useState(false)

  const access_token = localStorage.getItem("access_token")


  // Fetch dos Rate Limits
  const fetchRateLimits = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/rate-limits`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
      });

      if (response.ok) {
        const data = await response.json()
        setRateLimits(data)
      } else {
        setRateLimits({ error: "Falha ao carregar rate limits" })
      }
    } catch (error) {
      setRateLimits({ error: String(error) })
    }
  }

  // Atualiza automaticamente ao montar o componente
  useEffect(() => {
    fetchRateLimits()
    const interval = setInterval(fetchRateLimits, 60 * 1000) // atualizar a cada 1min
    return () => clearInterval(interval)
  }, [])

  const handleReprocessPR = async () => {
    if (!prNumber.trim()) {
      toast({
        title: "Erro",
        description: "Por favor, insira um número de PR válido",
        variant: "destructive"
      })
      return
    }

    setIsProcessing(true)
    try {

      const payload = { redoMerge }
 
      const response = await fetch(`${backendUrl}/api/reprocess-pr/${prNumber}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
        body: JSON.stringify(payload)
      });
      if (response.ok) {
        toast({
          title: "Sucesso",
          description: `PR #${prNumber} foi enviado para reprocessamento`,
          variant: "default"
        })
        setPrNumber("")
      } else {
        throw new Error('Falha na requisição')
      }
    } catch (error) {
      toast({
        title: "Erro",
        description: "Falha ao reprocessar o PR. Verifique os logs para mais detalhes.",
        variant: "destructive"
      })
    } finally {
      setIsProcessing(false)
    }
  }

  const testSystemHealth = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
      });


      if (response.ok) {
        const data = await response.json()
        toast({
          title: "Sistema Saudável",
          description: `Sistema operando normalmente. Status: ${data.status}`,
          variant: "default"
        })
      } else {
        throw new Error('Health check failed')
      }
    } catch (error) {
      toast({
        title: "Alerta de Sistema",
        description: "Possíveis problemas detectados no sistema. Verifique os logs.",
        variant: "destructive"
      })
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Controles do Sistema</h1>
        <p className="text-muted-foreground">
          Ações manuais e controles avançados para o sistema de IA
        </p>
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card className="bg-card shadow-card border-border">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-success" />
              Teste de Sistema
            </CardTitle>
            <CardDescription>
              Verificar saúde geral do sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button 
              onClick={testSystemHealth}
              variant="success"
              className="w-full"
            >
              <Play className="h-4 w-4 mr-2" />
              Executar Teste
            </Button>
          </CardContent>
        </Card>

        <Card className="bg-card shadow-card border-border">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Rocket className="h-5 w-5 text-warning" />
              Status do Deploy
            </CardTitle>
            <CardDescription>
              Verificar último deploy
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="text-sm">
                <span className="text-muted-foreground">Último deploy:</span>
                <br />
                <span className="font-mono">2024-01-15 12:30:45</span>
              </div>
              <div className="text-sm">
                <span className="text-success">● Status: Ativo</span>
              </div>
            </div>
          </CardContent>
        </Card>


        {/* Rate Limits */}
        <Card className="bg-card shadow-card border-border">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5 text-primary" />
              Rate Limits
            </CardTitle>
            <CardDescription>
              Monitorar limites de API
            </CardDescription>
          </CardHeader>
          <CardContent>
            {!rateLimits ? (
              <div className="text-sm text-muted-foreground">Carregando...</div>
            ) : rateLimits.error ? (
              <div className="text-sm text-red-500">{rateLimits.error}</div>
            ) : (
              <div className="space-y-2">
                <div className="text-sm">
                  <span className="text-muted-foreground">GitHub API:</span>
                  <br />
                  {rateLimits.github ? (
                    <span className="font-mono">
                      {rateLimits.github.remaining} / {rateLimits.github.limit}
                      {" (reset: " + new Date(rateLimits.github.reset * 1000).toLocaleTimeString() + ")"}
                    </span>
                  ) : (
                    <span className="text-muted-foreground">Não disponível</span>
                  )}
                </div>
                <div className="text-sm">
                  <span className="text-muted-foreground">OpenAI API:</span>
                  <br />
                  {rateLimits.openai ? (
                    <span className="font-mono">
                      {rateLimits.openai.model}  {rateLimits.openai.RPM} RPM | {rateLimits.openai.TPM} TPM | {rateLimits.openai.RPD} RPD
                    </span>
                  ) : (
                    <span className="text-muted-foreground">Não disponível</span>
                  )}

                </div>
                
              </div>
            )}
            <Button
              onClick={fetchRateLimits}
              variant="outline"
              size="sm"
              className="mt-3 w-full"
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Atualizar
            </Button>
          </CardContent>
        </Card>
        
      </div>

      {/* Main Controls */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Reprocess PR */}
        <Card className="bg-card shadow-card border-border">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <GitPullRequest className="h-5 w-5" />
              Reprocessar Pull Request
            </CardTitle>
            <CardDescription>
              Reprocessar um PR específico com a IA
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="pr-number">Número do PR</Label>
              <Input
                id="pr-number"
                placeholder="Ex: 1234"
                value={prNumber}
                onChange={(e) => setPrNumber(e.target.value)}
                type="number"
              />
            </div>
            <div className="flex items-center gap-2">
              <input
                id="redo-merge"
                type="checkbox"
                checked={redoMerge}
                onChange={(e) => setRedoMerge(e.target.checked)}
                className="h-4 w-4"
              />
              <Label htmlFor="redo-merge">Deseja refazer o Merge?</Label>
            </div>

            <Button 
              onClick={handleReprocessPR}
              disabled={isProcessing}
              variant="ai"
              className="w-full"
            >
              {isProcessing ? (
                <>
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  Processando...
                </>
              ) : (
                <>
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Reprocessar PR
                </>
              )}
            </Button>
          </CardContent>
        </Card>

      </div>

    </div>
  )
}

export default Controls