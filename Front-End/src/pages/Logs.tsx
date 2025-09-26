// Front-End\src\pages\Logs.tsx
import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { 
  RefreshCw, 
  Search, 
  Download,
  Play,
  Pause,
  Info,
  AlertTriangle,
  XCircle,
  Check
} from "lucide-react"

interface LogEntry {
  id: string
  timestamp: string
  level: "INFO" | "WARNING" | "ERROR"
  action: string
  details: string[]
  prNumber?: number
}

const Logs = () => {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [levelFilter, setLevelFilter] = useState<string>("all")
  const [autoRefresh, setAutoRefresh] = useState(true)
  const backendUrl = import.meta.env.VITE_BACK_END;


  const email = localStorage.getItem('user_email') || '';
  const password = localStorage.getItem('user_senha') || '';
  const access_token = localStorage.getItem("access_token")
  const payload = { email, password }
  const params = new URLSearchParams({ searchTerm, level: levelFilter, limit: "200", email, password });

  const fetchLogs = async () => {
    if (!email) return
    try {
      setIsLoading(true)
      const response = await fetch(`${backendUrl}/api/logs?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
      });

      const data = await response.json()
      setLogs(data)
    } catch (error) {
      console.error("Erro ao carregar logs:", error)
    } finally {
      setIsLoading(false)
    }
  }

  // Atualiza automaticamente ao montar o componente
  useEffect(() => {
    fetchLogs()
    const interval = setInterval(fetchLogs, 60 * 1000) // atualizar a cada 1min
    return () => clearInterval(interval)
  }, [])

  const getLevelBadge = (level: string) => {
    switch (level) {
      case "SUCCESS":
        return (
          <Badge variant="default" className="bg-green-500 text-white">
            <Check className="h-3 w-3 mr-1" />
            SUCCESS
          </Badge>
        )
      case "INFO":
        return (
          <Badge variant="default" className="bg-primary text-primary-foreground">
            <Info className="h-3 w-3 mr-1" />
            INFO
          </Badge>
        )
      case "WARNING":
        return (
          <Badge variant="secondary" className="bg-yellow-500 text-black">
            <AlertTriangle className="h-3 w-3 mr-1" />
            WARNING
          </Badge>
        )
      case "ERROR":
        return (
          <Badge variant="destructive">
            <XCircle className="h-3 w-3 mr-1" />
            ERROR
          </Badge>
        )

      default:
        return <Badge variant="outline">{level}</Badge>
    }
  }

  const exportLogs = async () => {
    if (!email) return
    try {

      const response = await fetch(`${backendUrl}/api/logs/export?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
      });


      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `logs-${new Date().toISOString().split("T")[0]}.txt`
      a.click()
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error("Erro ao exportar logs:", error)
    }
  }

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString("pt-BR")
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Logs do Sistema</h1>
          <p className="text-muted-foreground">Monitoramento em tempo real dos logs da aplicação</p>
        </div>
        <div className="flex items-center gap-2">
          {/* <Button
            onClick={() => setAutoRefresh(!autoRefresh)}
            variant={autoRefresh ? "neon" : "outline"}
            size="sm"
          >
            {autoRefresh ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
            {autoRefresh ? "Pausar" : "Iniciar"} Auto-refresh
          </Button> */}
          <Button onClick={fetchLogs} variant="outline" size="sm" disabled={isLoading}>
            <RefreshCw className="h-4 w-4" />
            Atualizar
          </Button>
          <Button onClick={exportLogs} variant="outline" size="sm">
            <Download className="h-4 w-4" />
            Exportar
          </Button>
        </div>
      </div>

      {/* Filtros */}
      <div className="flex gap-4">
        <Input
          placeholder="Buscar logs..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="max-w-sm"
        />
        <Select value={levelFilter} onValueChange={setLevelFilter}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Filtrar por nível" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Todos</SelectItem>
            <SelectItem value="INFO">INFO</SelectItem>
            <SelectItem value="WARNING">WARNING</SelectItem>
            <SelectItem value="ERROR">ERROR</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Lista de Logs */}
      <div className="space-y-2">
        {logs.map((log) => (
          <div key={log.id} className="p-3 rounded-lg border bg-card">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {getLevelBadge(log.level)}
                <span className="text-sm text-muted-foreground">{formatTimestamp(log.timestamp)}</span>
              </div>
              {log.prNumber && <span className="text-xs font-mono">PR #{log.prNumber}</span>}
            </div>
            <p className="mt-1 text-sm">{log.details.message}</p>
            <p className="text-xs text-muted-foreground">Action: {log.action}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Logs
