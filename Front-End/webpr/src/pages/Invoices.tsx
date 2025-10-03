import React, { useEffect, useState } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'

type Invoice = {
  id: string
  number: string
  date: string
  amount: number
  currency?: string
  status: 'paid' | 'pending' | 'failed'
  planName?: string
  pdfUrl?: string | null
  lines?: Array<{ description: string; qty?: number; price: number }>
}

const InvoicesPage = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [page, setPage] = useState(1)
  const [pageSize] = useState(12)
  const [total, setTotal] = useState(0)
  const [filterStatus, setFilterStatus] = useState<'all' | Invoice['status']>('all')
  const [query, setQuery] = useState('')
  const [selectedInvoice, setSelectedInvoice] = useState<Invoice | null>(null)

  const backend = import.meta.env.VITE_BACK_END || ''

  const accessToken = localStorage.getItem("access_token") || ""

  useEffect(() => {
    fetchInvoices()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, filterStatus])

  async function fetchInvoices() {
    setLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams()
      params.set('page', String(page))
      params.set('limit', String(pageSize))

      if (filterStatus !== 'all') params.set('status', filterStatus)
      if (query) params.set('q', query)

      const res = await fetch(`${backend}/api/invoices?${params.toString()}`, {
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': accessToken
        }
      })

      if (!res.ok) throw new Error('Falha ao buscar faturas')

      const body = await res.json()
      // Espera: { invoices: [...], total: number }
      setInvoices(body.invoices || [])
      setTotal(body.total || 0)
    } catch (err: any) {
      setError(err.message || 'Erro desconhecido')
    } finally {
      setLoading(false)
    }
  }

  function formatCurrency(v: number, currency = 'BRL') {
    try {
      return new Intl.NumberFormat('pt-BR', { style: 'currency', currency }).format(v)
    } catch {
      return `${v}`
    }
  }

  async function handleDownload(invoice: Invoice) {
    try {
      const res = await fetch(`${backend}/api/invoices/${invoice.id}/download`, {
        method: 'GET',
        headers: { 'X-API-TOKEN': accessToken }
      })

      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        if (body.pdfUrl) {
          // redirecionamento para URL externa
          window.open(body.pdfUrl, '_blank')
          return
        }
        throw new Error(body.error || 'Falha ao baixar fatura')
      }

      // Resposta é PDF direto
      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `invoice-${invoice.number}.pdf`
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
    } catch (err: any) {
      setError(err.message || 'Erro ao baixar fatura')
    }

  }

  async function handleView(invoice: Invoice) {
    const params = new URLSearchParams()

    if (!invoice.lines) {
      try {
        const res = await fetch(`${backend}/api/invoices/${invoice.id}`, {
          headers: {
            'X-API-TOKEN': accessToken
          }
        })
        if (res.ok) {
          const body = await res.json()
          setSelectedInvoice({ ...invoice, ...body })
          return
        }
      } catch (e) {
      }
    }
    setSelectedInvoice(invoice)
  }

  function closeModal() {
    setSelectedInvoice(null)
  }

  const totalPages = Math.max(1, Math.ceil(total / pageSize))

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">Faturas</h2>
        <div className="flex gap-2">
          <Button variant="ghost" onClick={() => window.history.back()}>Voltar</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <Input placeholder="Buscar por número ou descrição" value={query} onChange={e => setQuery(e.target.value)} />
        <Select value={filterStatus} onChange={(e: any) => { setFilterStatus(e.target.value as any); setPage(1) }}>
          <option value="all">Todos</option>
          <option value="paid">Pagas</option>
          <option value="pending">Pendentes</option>
          <option value="failed">Falhas</option>
        </Select>
        <div className="flex justify-end">
          <Button onClick={() => { setPage(1); fetchInvoices() }}>Atualizar</Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Lista de faturas</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div>Carregando faturas...</div>
          ) : error ? (
            <div className="text-destructive-foreground bg-destructive p-2 rounded">{error}</div>
          ) : invoices.length === 0 ? (
            <div>Sem faturas encontradas.</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="text-left text-muted-foreground">
                  <tr>
                    <th className="p-2">#</th>
                    <th className="p-2">Data</th>
                    <th className="p-2">Plano</th>
                    <th className="p-2">Valor</th>
                    <th className="p-2">Status</th>
                    <th className="p-2">Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {invoices.map(inv => (
                    <tr key={inv.id} className="border-t">
                      <td className="p-2 align-top">{inv.number}</td>
                      <td className="p-2 align-top">{new Date(inv.date).toLocaleString()}</td>
                      <td className="p-2 align-top">{inv.planName || '—'}</td>
                      <td className="p-2 align-top">{formatCurrency(inv.amount, inv.currency || 'BRL')}</td>
                      <td className="p-2 align-top">{inv.status}</td>
                      <td className="p-2 align-top">
                        <div className="flex gap-2">
                          <Button size="sm" onClick={() => handleView(inv)}>Ver</Button>
                          <Button size="sm" variant="outline" onClick={() => handleDownload(inv)}>Baixar</Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="flex items-center justify-between mt-4">
                <div className="text-sm">Mostrando {invoices.length} de {total} faturas</div>
                <div className="flex gap-2">
                  <Button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>Anterior</Button>
                  <div className="px-3 py-2 bg-muted rounded">{page} / {totalPages}</div>
                  <Button onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page === totalPages}>Próximo</Button>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Modal simples de fatura */}
      {selectedInvoice && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
          <div className="bg-background rounded-lg shadow-lg w-full max-w-2xl overflow-auto">
            <div className="p-4 border-b flex items-start justify-between">
              <div>
                <h3 className="text-lg font-semibold">Fatura #{selectedInvoice.number}</h3>
                <div className="text-sm text-muted-foreground">{new Date(selectedInvoice.date).toLocaleString()}</div>
              </div>
              <div className="flex gap-2">
                <Button onClick={() => handleDownload(selectedInvoice)}>Baixar PDF</Button>
                <Button variant="ghost" onClick={closeModal}>Fechar</Button>
              </div>
            </div>

            <div className="p-4">
              <div className="mb-4">
                <strong>Plano:</strong> {selectedInvoice.planName || '—'}
              </div>
              <div className="mb-4">
                <strong>Valor:</strong> {formatCurrency(selectedInvoice.amount, selectedInvoice.currency || 'BRL')}
              </div>

              <div>
                <strong>Itens:</strong>
                <ul className="mt-2 pl-4 list-disc">
                  {selectedInvoice.lines && selectedInvoice.lines.length > 0 ? (
                    selectedInvoice.lines.map((l, i) => (
                      <li key={i}>{l.description} — {l.qty ? `${l.qty} x ` : ''}{formatCurrency(l.price)}</li>
                    ))
                  ) : (
                    <li>Sem detalhamento disponível.</li>
                  )}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
export default InvoicesPage
