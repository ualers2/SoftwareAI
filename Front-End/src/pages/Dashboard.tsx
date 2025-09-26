import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

import { 
  Activity, 
  GitPullRequest, 
  CheckCircle, 
  XCircle, 
  Clock, 
  Zap,
  RefreshCw
} from "lucide-react"

interface SystemStats {
  totalPRs: number
  successfulPRs: number
  failedPRs: number
  pendingPRs: number
  uptime: string
  lastActivity: string
  tokensUsed: number
  tokenLimit: number
  tokenPercentUsed: number
  planName: string
  planExpiresAt: string
  planDaysLeft: number | null
}

interface RecentActivity {
  id: string
  type: string
  message: string
  timestamp: string
  status: "success" | "error" | "warning" | "info"
}

const Dashboard = () => {
  const [stats, setStats] = useState<SystemStats>({
    totalPRs: 0,
    successfulPRs: 0,
    failedPRs: 0,
    pendingPRs: 0,
    uptime: "0h 0m",
    lastActivity: "N/A",
    tokensUsed: 0,
    tokenLimit: 0,
    tokenPercentUsed: 0,
    planName: "Free",
    planExpiresAt: "N/A",
    planDaysLeft: null

  })
  
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([])
  const [isLoading, setIsLoading] = useState(true)

  const backendUrl = import.meta.env.VITE_BACK_END

  const email = localStorage.getItem('user_email') || '';
  const password = localStorage.getItem('user_senha') || '';
  const access_token = localStorage.getItem("access_token")
  const payload = { email, password }
  const params = new URLSearchParams({ email, password });

  const fetchDashboardData = async () => {
    if (!email) return
    try {
      setIsLoading(true)
      const response = await fetch(`${backendUrl}/api/dashboard-data?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
      });

      
      if (!response.ok) {
        console.error('Erro ao buscar dashboard:', response.status, await response.text())
        return
      }

      const result = await response.json()

      if (result && result.stats) {
        setStats({
          totalPRs: result.stats.totalPRs ?? 0,
          successfulPRs: result.stats.successfulPRs ?? 0,
          failedPRs: result.stats.failedPRs ?? 0,
          pendingPRs: result.stats.pendingPRs ?? 0,
          uptime: result.stats.uptime ?? "0h 0m",
          lastActivity: result.stats.lastActivity ?? "N/A",
          tokensUsed: result.stats.tokensUsed ?? 0,
          tokenLimit: result.stats.tokenLimit ?? 0,
          tokenPercentUsed: result.stats.tokenPercentUsed ?? 0,
          planName: result.stats.planName ?? "Free",
          planExpiresAt: result.stats.planExpiresAt ?? "N/A",
          planDaysLeft: result.stats.planDaysLeft ?? null
        })
      }
      setRecentActivity(Array.isArray(result.recentActivity) ? result.recentActivity : [])

    } catch (error) {
      console.error("Erro ao carregar dashboard:", error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchDashboardData()
    // Atualizar dados a cada 30 segundos
    const interval = setInterval(fetchDashboardData, 30000)
    return () => clearInterval(interval)
  }, [])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "success":
        return <CheckCircle className="h-4 w-4 text-success" />
      case "error":
        return <XCircle className="h-4 w-4 text-destructive" />
      case "warning":
        return <Clock className="h-4 w-4 text-warning" />
      default:
        return <Activity className="h-4 w-4" />
    }
  }

  const successRateText = () => {
    if (stats.totalPRs <= 0) return "0.0%"
    return `${((stats.successfulPRs / stats.totalPRs) * 100).toFixed(1)}%`
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground">
            Visão geral do sistema de IA para Pull Requests
          </p>
        </div>
        <Button 
          onClick={fetchDashboardData}
          variant="outline"
          size="sm"
          disabled={isLoading}
        >
          <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
          Atualizar
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="bg-card shadow-card border-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total PRs</CardTitle>
            <GitPullRequest className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary">{stats.totalPRs}</div>
            <p className="text-xs text-muted-foreground">
              PRs processados
            </p>
          </CardContent>
        </Card>

        <Card className="bg-card shadow-card border-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Sucessos</CardTitle>
            <CheckCircle className="h-4 w-4 text-success" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-success">{stats.successfulPRs}</div>
            <p className="text-xs text-muted-foreground">
              {successRateText()} taxa de sucesso
            </p>
          </CardContent>
        </Card>

        <Card className="bg-card shadow-card border-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Erros</CardTitle>
            <XCircle className="h-4 w-4 text-destructive" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-destructive">{stats.failedPRs}</div>
            <p className="text-xs text-muted-foreground">
              Necessitam atenção
            </p>
          </CardContent>
        </Card>

        <Card className="bg-card shadow-card border-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Uptime</CardTitle>
            <Zap className="h-4 w-4 text-warning" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-warning">{stats.uptime}</div>
            <p className="text-xs text-muted-foreground">
              Sistema ativo
            </p>
          </CardContent>
        </Card>

        <Card className="bg-card shadow-card border-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Consumo de Tokens</CardTitle>
            <Zap className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary">
              {stats.tokensUsed.toLocaleString()} / {stats.tokenLimit.toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              {stats.tokenPercentUsed}% do plano usado
            </p>
          </CardContent>
        </Card>
        
        <Card className="bg-card shadow-card border-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Plano Atual</CardTitle>
            <Zap className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary">{stats.planName}</div>
            <p className="text-xs text-muted-foreground">
              Expira em {stats.planExpiresAt}
              {stats.planDaysLeft !== null && ` (${stats.planDaysLeft} dias restantes)`}
            </p>
          </CardContent>
        </Card>

      </div>

      {/* Recent Activity */}
      <Card className="bg-card shadow-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Atividade Recente
          </CardTitle>
          <CardDescription>
            Últimas ações realizadas pelo sistema
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentActivity.length > 0 ? (
              recentActivity.map((activity) => (
                <div 
                  key={activity.id}
                  className="flex items-center justify-between p-3 rounded-lg bg-muted/50 border border-border/50"
                >
                  <div className="flex items-center gap-3">
                    {getStatusIcon(activity.status)}
                    <div>
                      <p className="text-sm font-medium text-foreground">
                        {activity.message}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {activity.timestamp}
                      </p>
                    </div>
                  </div>
                  <Badge 
                    variant={activity.status === "success" ? "default" : 
                            activity.status === "error" ? "destructive" : "secondary"}
                  >
                    {activity.type.replace("_", " ")}
                  </Badge>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                <Activity className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Nenhuma atividade recente</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard
