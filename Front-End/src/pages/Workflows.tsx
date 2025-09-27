// src/pages/Workflows.tsx
import { useEffect, useMemo, useState } from 'react'
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Search, Download, FileText, Info ,  RefreshCw} from 'lucide-react'

interface Workflow {
  id: string
  name: string
  category?: string
  createdAt?: string // ISO string
  yaml?: string
}

function RefreshIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4 mr-2">
      <path d="M21 2v6h-6"></path>
      <path d="M3 12a9 9 0 0 0 15.5 6.5L21 18"></path>
    </svg>
  )
}
const Workflows = () => {
  const [workflows, setWorkflows] = useState<Workflow[]>([])
  const [filtered, setFiltered] = useState<Workflow[]>([])
  const [query, setQuery] = useState('')
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showModal, setShowModal] = useState(false)

  const load = async () => {
    try {
        setLoading(true)
        setError(null)




        const backendUrl = import.meta.env.VITE_BACK_END

        const token = localStorage.getItem('access_token') ?? ''

        if (!token) {
            throw new Error('Email do usuário não encontrado. Verifique se há user_email no localStorage.')
        }


        const res = await fetch(`${backendUrl}/api/workflows`, {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json',
            'X-API-TOKEN': token,
            },
        })

        if (!res.ok) {
            const text = await res.text().catch(() => '')
            throw new Error(`Erro ao buscar workflows: ${res.status} ${text}`)
        }

        const result = await res.json()
        const list: Workflow[] = Array.isArray(result.workflows) ? result.workflows : (result || [])
        setWorkflows(list)
        setFiltered(list)
    } catch (err: any) {
      console.error(err)
      setError(err.message || 'Erro desconhecido')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  useEffect(() => {
    if (!query) return setFiltered(workflows)
    const q = query.toLowerCase()
    setFiltered(
      workflows.filter((w) =>
        (w.name || '').toLowerCase().includes(q) ||
        (w.category || '').toLowerCase().includes(q)
      )
    )
  }, [query, workflows])

  const selected = useMemo(() => workflows.find((w) => w.id === selectedId) ?? null, [workflows, selectedId])

  const openDetails = (id: string) => {
    setSelectedId(id)
    setShowModal(true)
  }

  const exportYaml = (wf: Workflow | null) => {
    if (!wf) return
    const filename = `${(wf.name || 'workflow').replace(/[^a-z0-9-_\.]/gi, '_')}.yaml`
    const content = wf.yaml ?? ''
    const blob = new Blob([content], { type: 'text/yaml;charset=utf-8' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Workflows</h1>
          <p className="text-sm text-muted-foreground">Pesquisar, visualizar e exportar .yaml dos workflows</p>
        </div>
        <div className="flex items-center gap-2">
          <Input
            placeholder="Pesquisar por nome, categoria ou git..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-80"
          />
          <Button onClick={load} variant="outline" disabled={loading}>
            <RefreshCw />
            Recarregar
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Lista de Workflows</CardTitle>
          <CardDescription>Selecione um workflow para ver detalhes ou exportar o .yaml</CardDescription>
        </CardHeader>
        <CardContent>
          {error && <div className="text-destructive mb-2">{error}</div>}

          <div className="grid gap-2">
            {loading ? (
              <div className="text-sm text-muted-foreground">Carregando...</div>
            ) : filtered.length === 0 ? (
              <div className="text-sm text-muted-foreground">Nenhum workflow encontrado</div>
            ) : (
              filtered.map((wf) => (
                <div
                  key={wf.id}
                  className={`flex items-center justify-between p-3 rounded border ${selectedId === wf.id ? 'border-primary bg-primary/5' : 'border-border bg-card'}`}
                >
                  <div className="flex items-center gap-3">
                    <div className="flex flex-col">
                      <div className="font-medium">{wf.name}</div>
                      <div className="text-xs text-muted-foreground">{wf.category || '—'}</div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Button size="sm" variant={selectedId === wf.id ? 'secondary' : 'ghost'} onClick={() => setSelectedId(wf.id)}>
                      Selecionar
                    </Button>

                    <Button size="sm" onClick={() => openDetails(wf.id)}>
                      <Info className="mr-2 h-3 w-3" /> Detalhes
                    </Button>

                    <Button size="sm" onClick={() => exportYaml(wf)}>
                      <Download className="mr-2 h-3 w-3" /> Exportar
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {/* Modal simples */}
      {showModal && selected && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-black/50" onClick={() => setShowModal(false)} />
          <div className="relative w-11/12 max-w-4xl p-6 bg-card rounded-lg shadow-lg z-10">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-xl font-semibold">{selected.name}</h2>
                <div className="text-sm text-muted-foreground">Categoria: {selected.category || '—'}</div>
                <div className="text-sm text-muted-foreground">Criado em: {selected.createdAt ? new Date(selected.createdAt).toLocaleString('pt-BR') : 'N/A'}</div>
              </div>
              <div className="flex items-center gap-2">
                <Button onClick={() => exportYaml(selected)}>
                  <Download className="mr-2 h-4 w-4" /> Exportar YAML
                </Button>
                <Button variant="ghost" onClick={() => setShowModal(false)}>Fechar</Button>
              </div>
            </div>

            <div className="mt-4">
              <div className="mb-2 font-medium">YAML do Workflow</div>
              <pre className="max-h-96 overflow-auto p-4 bg-muted rounded text-sm whitespace-pre-wrap break-words">
                {selected.yaml ?? 'Sem conteúdo YAML disponível.'}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}


export default Workflows

