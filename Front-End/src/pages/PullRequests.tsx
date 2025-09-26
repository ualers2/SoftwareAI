// Front-End\src\pages\PullRequests.tsx
import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { 
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { 
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { 
  GitPullRequest, 
  ExternalLink, 
  Eye, 
  RefreshCw,
  Search,
  Calendar,
  CheckCircle,
  XCircle,
  Clock
} from "lucide-react"

interface PullRequest {
  id: string
  number: number
  title: string
  status: "success" | "error" | "pending"
  processedAt: string
  githubUrl: string
  author: string
  aiGeneratedContent: string
  originalDiff: string
  total_tokens: string
  errorMessage?: string
}

const PullRequests = () => {
  const [prs, setPrs] = useState<PullRequest[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedPR, setSelectedPR] = useState<PullRequest | null>(null)
  const backendUrl = import.meta.env.VITE_BACK_END

  const email = localStorage.getItem('user_email') || '';
  const password = localStorage.getItem('user_senha') || '';
  const access_token = localStorage.getItem("access_token")
  const payload = { email, password }
  const params = new URLSearchParams({ email, password });
  const [showFullDiff, setShowFullDiff] = useState(false)

  const fetchPRs = async () => {
    if (!email) return
    try {
      setIsLoading(true)
      const res = await fetch(`${backendUrl}/api/pull-requests?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
      });
      if (!res.ok) throw new Error("Falha ao buscar PRs")


      const data: PullRequest[] = (await res.json()).map(pr => ({
        ...pr,
        author: pr.author ?? ""
      }))
      setPrs(data)
    } catch (error) {
      console.error("Erro ao carregar PRs:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const fetchPRDetails = async (prId: string) => {
    if (!email) return
    try {
      const res = await fetch(`${backendUrl}/api/pull-requests/${prId}?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
      });
      if (!res.ok) throw new Error("Falha ao buscar detalhes do PR")

      const data: PullRequest = await res.json()
      setSelectedPR(data)
    } catch (error) {
      console.error("Erro ao carregar detalhes do PR:", error)
    }
  }

  useEffect(() => {
    fetchPRs()
  }, [])

  const filteredPRs = prs.filter(pr => {
    const title = pr.title?.toString().toLowerCase() ?? ""
    const author = pr.author?.toString().toLowerCase() ?? ""
    const number = pr.number.toString()
    const term = searchTerm.toLowerCase()

    return title.includes(term) || number.includes(searchTerm) || author.includes(term)
  })


  const getStatusBadge = (status: string) => {
    switch (status) {
      case "completed":
        return (
          <Badge variant="default" className="bg-success text-success-foreground">
            <CheckCircle className="h-3 w-3 mr-1" /> Concluído
          </Badge>
        )
      case "error":
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
      case "processing":
        return (
          <Badge variant="outline" className="bg-yellow-200 text-yellow-800">
            <RefreshCw className="h-3 w-3 mr-1 animate-spin" /> Processando
          </Badge>
        )
      default:
        return <Badge variant="outline">Desconhecido</Badge>
    }
  }

  const formatDate = (dateString: string) => new Date(dateString).toLocaleString('pt-BR')


  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Pull Requests</h1>
          <p className="text-muted-foreground">Monitoramento e gerenciamento de PRs processados pela IA</p>
        </div>
        <Button onClick={fetchPRs} variant="ai" size="sm" disabled={isLoading}>
          <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} /> Atualizar
        </Button>
      </div>

      {/* Search */}
      <Card className="bg-card shadow-card border-border">
        <CardContent className="pt-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Buscar por número, título ou autor do PR..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </CardContent>
      </Card>

      {/* PRs Table */}
      <Card className="bg-card shadow-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <GitPullRequest className="h-5 w-5" /> Pull Requests ({filteredPRs.length})
          </CardTitle>
          <CardDescription>Lista de todos os PRs processados pelo sistema</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border border-border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>PR</TableHead>
                  <TableHead>Título</TableHead>
                  <TableHead>Autor</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Processado em</TableHead>
                  <TableHead className="text-right">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredPRs.length > 0 ? (
                  filteredPRs.map((pr) => (
                    <TableRow key={pr.id}>
                      <TableCell className="font-mono">#{pr.number}</TableCell>
                      <TableCell className="font-medium">{pr.title}</TableCell>
                      <TableCell>{pr.author}</TableCell>
                      <TableCell>{getStatusBadge(pr.status)}</TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1 text-sm text-muted-foreground">
                          <Calendar className="h-3 w-3" /> {formatDate(pr.processedAt)}
                        </div>
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex items-center justify-end gap-2">
                          <Dialog>
                            <DialogTrigger asChild>
                              <Button variant="outline" size="sm" onClick={() => fetchPRDetails(pr.id)}>
                                <Eye className="h-4 w-4" />
                              </Button>
                            </DialogTrigger>
                            <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
                              <DialogHeader>
                                <DialogTitle>PR #{selectedPR?.number} - {selectedPR?.title}</DialogTitle>
                                <DialogDescription>Detalhes completos do Pull Request processado</DialogDescription>
                              </DialogHeader>
                              {selectedPR && (
                                <div className="space-y-4">
                                  <div className="grid grid-cols-2 gap-4">
                                    <div>
                                      <h4 className="font-semibold mb-2">Informações</h4>
                                      <div className="space-y-2 text-sm">
                                        <p><strong>Status:</strong> {getStatusBadge(selectedPR.status)}</p>
                                        <p><strong>Autor:</strong> {selectedPR.author}</p>
                                        <p><strong>Processado:</strong> {formatDate(selectedPR.processedAt)}</p>
                                        <p><strong>Tokens Consumidos:</strong> {selectedPR.total_tokens}</p>
                                      </div>
                                    </div>
                                    <div>
                                      <h4 className="font-semibold mb-2">Links</h4>
                                      <Button variant="outline" size="sm" asChild>
                                        <a href={selectedPR.githubUrl} target="_blank" rel="noopener noreferrer">
                                          <ExternalLink className="h-4 w-4 mr-2" /> Ver no GitHub
                                        </a>
                                      </Button>
                                    </div>
                                  </div>
                                  {selectedPR.errorMessage && (
                                    <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
                                      <h4 className="font-semibold text-destructive mb-2">Erro</h4>
                                      <p className="text-sm">{selectedPR.errorMessage}</p>
                                    </div>
                                  )}
                                  <div>
                                    <h4 className="font-semibold mb-2">Conteúdo Gerado pela IA</h4>
                                    <div className="p-3 bg-muted rounded-lg max-h-64 overflow-y-auto max-w-full">
                                      <pre className="text-sm whitespace-pre-wrap break-all max-w-full">
                                        {selectedPR.aiGeneratedContent || "Nenhum conteúdo gerado"}
                                      </pre>
                                    </div>
                                  </div>
                                  <div>
                                    <h4 className="font-semibold mb-2">Diff Original</h4>
                                    <div className="p-3 bg-muted rounded-lg max-w-full">
                                      <pre className="text-sm font-mono whitespace-pre-wrap break-all max-w-full">
                                        {showFullDiff
                                          ? selectedPR.originalDiff
                                          : selectedPR.originalDiff.slice(0, 300) + 
                                            (selectedPR.originalDiff.length > 300 ? "..." : "")
                                        }
                                      </pre>
                                      {selectedPR.originalDiff.length > 300 && (
                                        <Button 
                                          variant="outline" 
                                          size="sm" 
                                          className="mt-2"
                                          onClick={() => setShowFullDiff(!showFullDiff)}
                                        >
                                          {showFullDiff ? "Mostrar menos" : "Carregar mais"}
                                        </Button>
                                      )}
                                    </div>

                                  </div>
                                </div>
                              )}
                            </DialogContent>
                          </Dialog>
                          <Button variant="outline" size="sm" asChild>
                            <a href={pr.githubUrl} target="_blank" rel="noopener noreferrer">
                              <ExternalLink className="h-4 w-4" />
                            </a>
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                      {searchTerm ? "Nenhum PR encontrado com os critérios de busca" : "Nenhum PR processado ainda"}
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


export default PullRequests
