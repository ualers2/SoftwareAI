// src/components/SignupCheckout.tsx
import React, { useState } from "react";
import { loadStripe } from "@stripe/stripe-js";
import { useSearchParams } from "react-router-dom";

const STRIPE_KEY = import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY || "";
const stripePromise = STRIPE_KEY ? loadStripe(STRIPE_KEY) : Promise.resolve(null);

export default function SignupCheckout(): JSX.Element {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [searchParams] = useSearchParams();
  const plan = searchParams.get("plan") || "Premium";
  const billingCycleParam = searchParams.get("billing") as "monthly" | "annual" | null;
  const [billingCycle] = useState<"monthly" | "annual">(billingCycleParam || "monthly");

  const priceParam = searchParams.get("price");
  const priceAmount = priceParam ? parseFloat(priceParam) : billingCycle === "annual" ? 88 : 8;
  const priceLabel = billingCycle === "annual" ? `$${priceAmount} / ano` : `$${priceAmount} / mês`;

  const VITE_API_URL = import.meta.env.VITE_BACK_END || "";

  function validateEmail(e: string) {
    return /\S+@\S+\.\S+/.test(e);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!validateEmail(email)) {
      setError("Informe um email válido.");
      return;
    }
    if (password.length < 4) {
      setError("Senha precisa ter 4 caracteres ou mais.");
      return;
    }
    if (!VITE_API_URL) {
      setError("Configuração de API ausente. Contate o time.");
      return;
    }

    setLoading(true);
    try {
      const resp = await fetch(`${VITE_API_URL}/api/billing/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          password,
          plan,
          billingCycle,
        }),
      });

      const body = await resp.json().catch(() => ({}));
      if (!resp.ok) throw new Error(body?.error || `Erro do servidor (${resp.status})`);

      if (body.sessionId) {
        const stripe = await stripePromise;
        if (stripe) {
          const result = await stripe.redirectToCheckout({ sessionId: body.sessionId });
          if ((result as any).error) {
            setError((result as any).error.message || "Erro ao redirecionar para o Stripe.");
          }
        } else {
          setError("Stripe não configurado no frontend.");
        }
      } else {
        setError("Resposta inesperada do servidor.");
      }
    } catch (err: any) {
      setError(err?.message || "Erro ao criar sessão.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-lg mx-auto card-glass p-8 rounded-2xl">
      {/* Header */}
      <div className="mb-8 text-center">
        <h2 className="text-3xl font-bold mb-2">Finalizar Assinatura</h2>
        <p className="text-muted-foreground">
          Você selecionou o plano <span className="font-semibold">{plan}</span> —{" "}
          <span className="text-primary">{priceLabel}</span>
        </p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-5" aria-live="polite">
        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input
            type="email"
            className="w-full rounded-lg border px-3 py-2 bg-background focus:outline-none focus:ring-2 focus:ring-primary"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="seu@exemplo.com"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Senha</label>
          <input
            type="password"
            className="w-full rounded-lg border px-3 py-2 bg-background focus:outline-none focus:ring-2 focus:ring-primary"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={4}
            placeholder="Mínimo 4 caracteres"
          />
          <p className="text-xs text-muted-foreground mt-1">Mínimo 4 caracteres</p>
        </div>

        {/* CTA */}
        <div>
          <button
            type="submit"
            className="btn-hero w-full flex items-center justify-center gap-2"
            disabled={loading}
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8v8z"
                  />
                </svg>
                Processando...
              </>
            ) : (
              <>Prosseguir — {priceLabel}</>
            )}
          </button>
          <p className="text-xs text-muted-foreground mt-2 text-center">
            Você será redirecionado para o checkout seguro do Stripe.
          </p>
        </div>

        {error && (
          <div className="text-sm text-red-600 mt-2 text-center" role="alert">
            {error}
          </div>
        )}
      </form>
    </div>
  );
}
