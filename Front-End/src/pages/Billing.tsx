import React, { useEffect, useState } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

type AccountData = {
  user_id: number
  email: string
  planName: string
  planExpiresAt: string | null
  tokensUsed: number
  tokenLimit: number
  remainingTokens: number
}

const samplePlans = [
  {
    id: 'free',
    name: 'Free',
    price: 'R$ 0/mês',
    features: ['300k tokens / mês', 'Suporte via docs', 'Limitações básicas']
  },
  {
    id: 'pro',
    name: 'Pro',
    price: 'R$ 49/mês',
    features: ['1M tokens / mês', 'Suporte por e-mail', 'Renovação automática']
  },
  {
    id: 'business',
    name: 'Business',
    price: 'R$ 249/mês',
    features: ['Tokens ilimitados', 'Suporte prioritário', 'Conta multi-usuário']
  }
]

const BillingPage = () => {
  const [account, setAccount] = useState<AccountData | null>(null)
  const [loading, setLoading] = useState(false)
  const [actionLoading, setActionLoading] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const backend = import.meta.env.VITE_BACK_END || ''
  const email = localStorage.getItem("user_email") || ""
  const password = localStorage.getItem("user_senha") || ""
  const accessToken = localStorage.getItem("access_token") || ""

  useEffect(() => {
    fetchAccount()
  }, [])

  async function fetchAccount() {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${backend}/api/myaccount?email=${email}&password=${password}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': accessToken
        }
      })
      if (!res.ok) throw new Error('Falha ao buscar dados da conta')
      const data = await res.json()
      setAccount({
        user_id: data.user_id,
        email: data.email,
        planName: data.planName || 'Free',
        planExpiresAt: data.planExpiresAt || null,
        tokensUsed: data.tokensUsed || 0,
        tokenLimit: data.tokenLimit || 0,
        remainingTokens: data.remainingTokens || 0
      })
    } catch (err: any) {
      setError(err.message || 'Erro desconhecido')
    } finally {
      setLoading(false)
    }
  }

  function calcPercent(used: number, limit: number) {
    if (limit === 0) return 0
    return Math.min(100, Math.round((used / limit) * 100))
  }

  async function handleRenew() {
    if (!account) return
    setActionLoading('renew')
    try {
      const res = await fetch(`${backend}/api/renew-plan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': accessToken
        },
        body: JSON.stringify({ plan: account.planName })
      })
      if (!res.ok) throw new Error('Falha ao renovar o plano')
      await fetchAccount()
    } catch (err: any) {
      setError(err.message || 'Erro na renovação')
    } finally {
      setActionLoading(null)
    }
  }

  async function handleSubscribe(planId: string) {
    setActionLoading(planId)
    try {
      const res = await fetch(`${backend}/api/subscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': accessToken
        },
        body: JSON.stringify({ planId })
      })
      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.error || 'Falha ao assinar plano')
      }
      await fetchAccount()
    } catch (err: any) {
      setError(err.message || 'Erro ao assinar plano')
    } finally {
      setActionLoading(null)
    }
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Billing — Minha conta</h2>

      {error && (
        <div className="mb-4 text-sm text-destructive-foreground bg-destructive p-2 rounded">{error}</div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column: account summary */}
        <div className="lg:col-span-1 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Plano atual</CardTitle>
            </CardHeader>
            <CardContent>
              {loading || !account ? (
                <div>Carregando...</div>
              ) : (
                <>
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-lg font-semibold">{account.planName}</div>
                      <div className="text-sm text-muted-foreground">Expira em: {account.planExpiresAt ?? 'N/A'}</div>
                    </div>
                    <div>
                      <Badge>{account.remainingTokens} tokens restantes</Badge>
                    </div>
                  </div>

                  <div className="mt-4">
                    <div className="text-sm mb-2">Uso de tokens: {account.tokensUsed} / {account.tokenLimit}</div>
                    <div className="w-full bg-muted rounded h-3 overflow-hidden">
                      <div style={{ width: `${calcPercent(account.tokensUsed, account.tokenLimit)}%` }} className="h-3 bg-primary" />
                    </div>
                    <div className="mt-3 flex gap-2">
                      <Button onClick={handleRenew} disabled={actionLoading !== null}>
                        {actionLoading === 'renew' ? 'Renovando...' : 'Renovar plano'}
                      </Button>
                    </div>
                  </div>
                </>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Tokens consumidos</CardTitle>
            </CardHeader>
            <CardContent>
              {account ? (
                <>
                  <div className="text-3xl font-bold">{account.tokensUsed}</div>
                  <div className="text-sm text-muted-foreground">Limite: {account.tokenLimit}</div>
                  <div className="mt-3 w-full bg-muted rounded h-3 overflow-hidden">
                    <div style={{ width: `${calcPercent(account.tokensUsed, account.tokenLimit)}%` }} className="h-3 bg-primary" />
                  </div>
                </>
              ) : (
                <div>—</div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Ações</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-2">
                <Button onClick={() => window.open('/billing/invoices', '_self')}>Ver faturas</Button>
                <Button variant="ghost" onClick={() => window.open('/support', '_self')}>Contatar suporte</Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right column: plans */}
        <div className="lg:col-span-2">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {samplePlans.map((p) => (
              <Card key={p.id} className="flex flex-col">
                <CardHeader>
                  <CardTitle>{p.name}</CardTitle>
                </CardHeader>
                <CardContent className="flex-1 flex flex-col justify-between">
                  <div>
                    <div className="text-xl font-semibold mb-2">{p.price}</div>
                    <ul className="mb-4 text-sm space-y-1">
                      {p.features.map((f, i) => (
                        <li key={i}>• {f}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="mt-4">
                    <Button onClick={() => handleSubscribe(p.id)} disabled={actionLoading !== null}>
                      {actionLoading === p.id ? 'Processando...' : p.id === 'free' ? 'Selecionar' : `Assinar ${p.name}`}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>

    </div>
  )
}

export default BillingPage
