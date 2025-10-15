import { useEffect, useState } from "react"
import { 
  Card, CardContent, CardHeader, CardTitle, CardDescription 
} from "@/components/ui/card"
import { 
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow 
} from "@/components/ui/table"
import { 
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogTrigger 
} from "@/components/ui/dialog"
import { 
  Button 
} from "@/components/ui/button"
import { 
  Badge 
} from "@/components/ui/badge"
import { 
  Input 
} from "@/components/ui/input"
import { 
  ClipboardList, 
  RefreshCw, 
  Eye, 
  Search, 
  Calendar, 
  Clock, 
  CheckCircle, 
  XCircle,
  CalendarClock 
} from "lucide-react"

interface Task {
  id: string
  content: string
  priority: number
  status: "pending" | "processing" | "completed" | "error"
  createdAt: string
  completedAt?: string | null
  eta_str?: string | null
  estimatedHours: string
  commitLanguage: string
  result?: string | null
}

const AgentTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([])
  const [selectedTask, setSelectedTask] = useState<Task | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [showFullContent, setShowFullContent] = useState(false)
  const backendUrl = import.meta.env.VITE_BACK_END
  const access_token = localStorage.getItem("access_token")

  const fetchTasks = async () => {
    if (!access_token) return
    try {
      setIsLoading(true)
      const res = await fetch(`${backendUrl}/api/tasks/list`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
      })
      if (!res.ok) throw new Error("Falha ao carregar tarefas")

      const data: Task[] = await res.json()
      setTasks(data)
    } catch (error) {
      console.error("Erro ao buscar tarefas:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const fetchTaskDetails = async (taskId: string) => {
    if (!access_token) return
    try {
      const res = await fetch(`${backendUrl}/api/tasks/details/${taskId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
      })
      if (!res.ok) throw new Error("Falha ao buscar detalhes da tarefa")

      const data: Task = await res.json()
      setSelectedTask(data)
    } catch (error) {
      console.error("Erro ao buscar detalhes da tarefa:", error)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [])

  const filteredTasks = tasks.filter(task =>
    task.content.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "done":
        return (
          <Badge variant="default" className="bg-success text-success-foreground">
            <CheckCircle className="h-3 w-3 mr-1" /> Concluída
          </Badge>
        )
      case "failed":
        return (
          <Badge variant="destructive">
            <XCircle className="h-3 w-3 mr-1" /> Erro
          </Badge>
        )
      case "pending":
        return (
          <Badge variant="secondary">
            <Clock className="h-3 w-3 mr-1" /> Pendente
          </Badge>
        )
      case "running":
        return (
          <Badge variant="outline" className="bg-yellow-200 text-yellow-800">
            <RefreshCw className="h-3 w-3 mr-1 animate-spin" /> Processando
          </Badge>
        )
      case "sheduled":
        return (
          <Badge variant="outline" className="bg-yellow-200 text-yellow-800">
            <CalendarClock className="h-3 w-3 mr-1 animate-spin" /> Agendada
          </Badge>
        )
      default:
        return <Badge variant="outline">Desconhecido</Badge>
    }
  }

  const formatDate = (dateString?: string | null) =>
    dateString ? new Date(dateString).toLocaleString('pt-BR') : "—"

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Tarefas dos Agentes</h1>
          <p className="text-muted-foreground">Monitoramento e histórico de tarefas processadas pela IA</p>
        </div>
        <Button onClick={fetchTasks} variant="ai" size="sm" disabled={isLoading}>
          <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} /> Atualizar
        </Button>
      </div>

      {/* Search */}
      <Card className="bg-card shadow-card border-border">
        <CardContent className="pt-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Buscar por conteúdo da tarefa..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </CardContent>
      </Card>

      {/* Tasks Table */}
      <Card className="bg-card shadow-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ClipboardList className="h-5 w-5" /> Tarefas ({filteredTasks.length})
          </CardTitle>
          <CardDescription>Lista das tarefas criadas e processadas</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border border-border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Conteúdo</TableHead>
                  <TableHead>Prioridade</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Criada em</TableHead>
                  <TableHead>Agendada para</TableHead>
                  <TableHead className="text-right">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredTasks.length > 0 ? (
                  filteredTasks.map(task => (
                    <TableRow key={task.id}>
                      <TableCell className="font-mono text-sm">{task.id.slice(0, 8)}</TableCell>
                      <TableCell className="max-w-[280px] truncate">{task.content}</TableCell>
                      <TableCell>{task.priority}</TableCell>
                      <TableCell>{getStatusBadge(task.status)}</TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1 text-sm text-muted-foreground">
                          <Calendar className="h-3 w-3" /> {formatDate(task.createdAt)}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1 text-sm text-muted-foreground">
                          <Calendar className="h-3 w-3" /> {formatDate(task.eta_str)}
                        </div>
                      </TableCell>
                      <TableCell className="text-right">
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => fetchTaskDetails(task.id)}
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
                            <DialogHeader>
                              <DialogTitle>Tarefa {task.id.slice(0, 8)}</DialogTitle>
                              <DialogDescription>Detalhes completos da tarefa processada</DialogDescription>
                            </DialogHeader>
                            {selectedTask && selectedTask.id === task.id && (
                              <div className="space-y-4">
                                <div className="grid grid-cols-2 gap-4">
                                  <div>
                                    <h4 className="font-semibold mb-2">Informações</h4>
                                    <div className="space-y-2 text-sm">
                                      <p><strong>Status:</strong> {getStatusBadge(selectedTask.status)}</p>
                                      <p><strong>Prioridade:</strong> {selectedTask.priority}</p>
                                      <p><strong>Linguagem:</strong> {selectedTask.commitLanguage}</p>
                                      <p><strong>Horas Estimada:</strong> {selectedTask.estimatedHours}</p>
                                      <p><strong>Criada em:</strong> {formatDate(selectedTask.createdAt)}</p>
                                      <p><strong>Agendada para:</strong> {formatDate(selectedTask.eta_str)}</p>
                                    </div>
                                  </div>
                                </div>

                                <div>
                                  <h4 className="font-semibold mb-2">Conteúdo Original</h4>
                                  <div className="p-3 bg-muted rounded-lg max-w-full">
                                    <pre className="text-sm whitespace-pre-wrap break-all max-w-full">
                                      {showFullContent
                                        ? selectedTask.content
                                        : selectedTask.content.slice(0, 300) + 
                                          (selectedTask.content.length > 300 ? "..." : "")
                                      }
                                    </pre>
                                    {selectedTask.content.length > 300 && (
                                      <Button
                                        variant="outline"
                                        size="sm"
                                        className="mt-2"
                                        onClick={() => setShowFullContent(!showFullContent)}
                                      >
                                        {showFullContent ? "Mostrar menos" : "Carregar mais"}
                                      </Button>
                                    )}
                                  </div>
                                </div>

                                {selectedTask.result && (
                                  <div>
                                    <h4 className="font-semibold mb-2">Resultado do Agente</h4>
                                    <div className="p-3 bg-muted rounded-lg max-h-64 overflow-y-auto">
                                      <pre className="text-sm whitespace-pre-wrap break-all">
                                        {selectedTask.result}
                                      </pre>
                                    </div>
                                  </div>
                                )}
                              </div>
                            )}
                          </DialogContent>
                        </Dialog>
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={7} className="text-center py-8 text-muted-foreground">
                      {searchTerm ? "Nenhuma tarefa encontrada" : "Nenhuma tarefa registrada ainda"}
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default AgentTasks
