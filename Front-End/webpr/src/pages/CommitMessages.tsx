import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { 
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow 
} from "@/components/ui/table"
import { 
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger , DialogDescription
} from "@/components/ui/dialog"
import { 
  GitCommit, ExternalLink, Eye, RefreshCw, Search, Calendar, CheckCircle, XCircle, Clock, 
  GitPullRequest
} from "lucide-react"

interface Commit {
  id: string
  title: string
  hash: string
  message: string
  status: "success" | "error" | "pending" | "processing"
  processedAt: string
  author: string
  aiGeneratedMessage: string
  originalDiff: string
  total_tokens: string
  errorMessage?: string
  linkedPR?: number
}

const CommitMessages = () => {
  const [commits, setCommits] = useState<Commit[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedCommit, setSelectedCommit] = useState<Commit | null>(null)
  const backendUrl = import.meta.env.VITE_BACK_END
  const access_token = localStorage.getItem("access_token")
  const [showFullDiff, setShowFullDiff] = useState(false)
  const fetchCommits = async () => {
    if (!access_token) return
    try {
      setIsLoading(true)
      const res = await fetch(`${backendUrl}/api/commit-messages`, {
        headers: { "Content-Type": "application/json", "X-API-TOKEN": `${access_token}` }
      })
      if (!res.ok) throw new Error("Falha ao buscar commits")
      const data: Commit[] = await res.json()
      setCommits(data)
    } catch (e) {
      console.error("Erro ao carregar commits:", e)
    } finally {
      setIsLoading(false)
    }
  }

  const fetchCommitDetails = async (commitId: string) => {
    if (!access_token) return
    try {
      const res = await fetch(`${backendUrl}/api/commit-messages/${commitId}`, {
        headers: { "Content-Type": "application/json", "X-API-TOKEN": `${access_token}` }
      })
      if (!res.ok) throw new Error("Falha ao buscar detalhes do commit")
      const data: Commit = await res.json()
      setSelectedCommit(data)
    } catch (e) {
      console.error("Erro ao carregar detalhes do commit:", e)
    }
  }

  useEffect(() => { fetchCommits() }, [])

  const filteredCommits = commits.filter(c => {
    const msg = c.message?.toLowerCase() ?? ""
    const author = c.author?.toLowerCase() ?? ""
    const hash = c.hash.toLowerCase()
    const term = searchTerm.toLowerCase()
    return msg.includes(term) || hash.includes(term) || author.includes(term)
  })

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "completed":
        return <Badge variant="default" className="bg-green-500 text-white"><CheckCircle className="h-3 w-3 mr-1"/>Concluído</Badge>
      case "error":
        return <Badge variant="destructive"><XCircle className="h-3 w-3 mr-1"/>Erro</Badge>
      case "pending":
        return <Badge variant="secondary"><Clock className="h-3 w-3 mr-1"/>Pendente</Badge>
      case "processing":
        return <Badge variant="outline" className="bg-yellow-200 text-yellow-800"><RefreshCw className="h-3 w-3 mr-1 animate-spin"/>Processando</Badge>
      default:
        return <Badge variant="outline">Desconhecido</Badge>
    }
  }

  const formatDate = (date: string) => new Date(date).toLocaleString("pt-BR")

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Commits</h1>
          <p className="text-muted-foreground">Gerenciamento de mensagens de commit processadas pela IA</p>
        </div>
        <Button onClick={fetchCommits} variant="ai" size="sm" disabled={isLoading}>
          <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} /> Atualizar
        </Button>
      </div>

      {/* Search */}
      <Card className="bg-card shadow-card border-border">
        <CardContent className="pt-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Buscar por hash, título ou autor do Commit..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </CardContent>
      </Card>

      {/* Commits Table */}
      <Card className="bg-card shadow-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <GitPullRequest className="h-5 w-5" /> Commits ({filteredCommits.length})
          </CardTitle>
          <CardDescription>Lista de todos os Commits processados pelo sistema</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border border-border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Commit Hash</TableHead>
                  <TableHead>Título</TableHead>
                  <TableHead>Autor</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Processado em</TableHead>
                  <TableHead className="text-right">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredCommits.length > 0 ? (
                  filteredCommits.map((commit) => (
                    <TableRow key={commit.id}>
                      <TableCell className="font-mono">{commit.hash.slice(0, 15)}</TableCell>
                      <TableCell className="font-medium">{commit.title}</TableCell>
                      <TableCell>{commit.author}</TableCell>
                      <TableCell>{getStatusBadge(commit.status)}</TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1 text-sm text-muted-foreground">
                          <Calendar className="h-3 w-3" /> {formatDate(commit.processedAt)}
                        </div>
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex items-center justify-end gap-2">
                          <Dialog>
                            <DialogTrigger asChild>
                              <Button variant="outline" size="sm" onClick={() => fetchCommitDetails(commit.id)}>
                                <Eye className="h-4 w-4" />
                              </Button>
                            </DialogTrigger>
                            <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
                              <DialogHeader>
                                <DialogTitle>Commit #{selectedCommit?.title} </DialogTitle>
                                <DialogDescription>Detalhes completos do Commit Criado</DialogDescription>
                              </DialogHeader>
                              {selectedCommit && (
                                <div className="space-y-4">
                                  <div className="grid grid-cols-2 gap-4">
                                    <div>
                                      <h4 className="font-semibold mb-2">Informações</h4>
                                      <div className="space-y-2 text-sm">
                                        <p><strong>Status:</strong> {getStatusBadge(selectedCommit.status)}</p>
                                        <p><strong>Autor:</strong> {selectedCommit.author}</p>
                                        <p><strong>Processado:</strong> {formatDate(selectedCommit.processedAt)}</p>
                                        <p><strong>Tokens Consumidos:</strong> {selectedCommit.total_tokens}</p>
                                        <p><strong>Commit Hash:</strong> {selectedCommit.hash}</p>
                                      </div>
                                    </div>
                                    {/* <div>
                                      <h4 className="font-semibold mb-2">Links</h4>
                                      <Button variant="outline" size="sm" asChild>
                                        <a href={selectedCommit.githubUrl} target="_blank" rel="noopener noreferrer">
                                          <ExternalLink className="h-4 w-4 mr-2" /> Ver no GitHub
                                        </a>
                                      </Button>
                                    </div> */}
                                  </div>
                                  {selectedCommit.errorMessage && (
                                    <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
                                      <h4 className="font-semibold text-destructive mb-2">Erro</h4>
                                      <p className="text-sm">{selectedCommit.errorMessage}</p>
                                    </div>
                                  )}
                                  <div>
                                    <h4 className="font-semibold mb-2">Conteúdo Gerado pela IA</h4>
                                    <div className="p-3 bg-muted rounded-lg max-h-64 overflow-y-auto max-w-full">
                                      <pre className="text-sm whitespace-pre-wrap break-all max-w-full">
                                        {selectedCommit.aiGeneratedMessage || "Nenhum conteúdo gerado"}
                                      </pre>
                                    </div>
                                  </div>
                                  <div>
                                    <h4 className="font-semibold mb-2">Diff Original</h4>
                                    <div className="p-3 bg-muted rounded-lg max-w-full">
                                      <pre className="text-sm font-mono whitespace-pre-wrap break-all max-w-full">
                                        {showFullDiff
                                        ? (selectedCommit.originalDiff || "Nenhum diff disponível")
                                        : (selectedCommit.originalDiff 
                                            ? selectedCommit.originalDiff.slice(0, 300) + 
                                                (selectedCommit.originalDiff.length > 300 ? "..." : "")
                                            : "Nenhum diff disponível"
                                            )
                                        }
                                      </pre>
                                        {selectedCommit.originalDiff && selectedCommit.originalDiff.length > 300 && (
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
                          {/* <Button variant="outline" size="sm" asChild>
                            <a href={commit.githubUrl} target="_blank" rel="noopener noreferrer">
                              <ExternalLink className="h-4 w-4" />
                            </a>
                          </Button> */}
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


export default CommitMessages
