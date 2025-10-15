// webproject\src\components\MyAccount.tsx
import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Mail, Lock, Key, Zap, Calendar, RefreshCw } from "lucide-react"

interface AccountData {
  email: string
  password: string
  accessToken: string
  planExpiresAt: string
  tokensUsed: number
  tokenLimit: number
  tokenPercentUsed: number
}

const MyAccount = () => {
  const [account, setAccount] = useState<AccountData>({
    email: "",
    password: "",
    accessToken: "",
    planExpiresAt: "N/A",
    tokensUsed: 0,
    tokenLimit: 0,
    tokenPercentUsed: 0,
  })
  const [isLoading, setIsLoading] = useState(false)

  const backendUrl = import.meta.env.VITE_BACK_END
  const email = localStorage.getItem("user_email") || ""
  const password = localStorage.getItem("user_senha") || ""
  const accessToken = localStorage.getItem("access_token") || ""
  
  const fetchAccountData = async () => {
    if (!email || !accessToken) return
    try {
      setIsLoading(true)
      const response = await fetch(`${backendUrl}/api/myaccount`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "X-API-TOKEN": accessToken,
        },
      })

      if (!response.ok) {
        console.error("Erro ao buscar dados da conta:", response.status)
        return
      }

      const result = await response.json()
      setAccount({
        email,
        password,
        accessToken,
        planExpiresAt: result.planExpiresAt ?? "N/A",
        tokensUsed: result.tokensUsed ?? 0,
        tokenLimit: result.tokenLimit ?? 0,
        tokenPercentUsed: result.tokenPercentUsed ?? 0,
      })
    } catch (err) {
      console.error("Erro ao carregar conta:", err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchAccountData()
  }, [])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-foreground">Minha Conta</h1>
        <Button onClick={fetchAccountData} variant="outline" size="sm" disabled={isLoading}>
          <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />
          Atualizar
        </Button>
      </div>

      <Card className="shadow-lg border-border">
        <CardHeader>
          <CardTitle>Informações Pessoais</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium flex items-center gap-2">
              <Mail className="h-4 w-4" /> Email
            </label>
            <Input value={account.email} disabled />
          </div>

          <div>
            <label className="text-sm font-medium flex items-center gap-2">
              <Lock className="h-4 w-4" /> Senha
            </label>
            <Input type="password" value={account.password} disabled />
          </div>

          <div>
            <label className="text-sm font-medium flex items-center gap-2">
                <Key className="h-4 w-4" /> API Token
            </label>
            <div className="flex gap-2">
                <Input value={account.accessToken} disabled />
                <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => navigator.clipboard.writeText(account.accessToken)}
                >
                Copiar
                </Button>
            </div>
          </div>

        </CardContent>
      </Card>

      <Card className="shadow-lg border-border">
        <CardHeader>
          <CardTitle>Plano & Tokens</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="flex items-center gap-2 text-sm font-medium">
              <Calendar className="h-4 w-4" /> Expiração do Plano
            </span>
            <Badge variant="secondary">{account.planExpiresAt}</Badge>
          </div>

          <div className="flex justify-between items-center">
            <span className="flex items-center gap-2 text-sm font-medium">
              <Zap className="h-4 w-4" /> Tokens Consumidos
            </span>
            <span className="text-sm">
              {account.tokensUsed.toLocaleString()} / {account.tokenLimit.toLocaleString()} (
              {account.tokenPercentUsed}%)
            </span>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default MyAccount
