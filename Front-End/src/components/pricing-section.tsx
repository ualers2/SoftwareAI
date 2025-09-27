import { Check, Star, Zap } from "lucide-react";
import { useEffect, useState } from "react";
import { project } from "@/constants/landingpage.ts";

export const PricingSection = () => {
  const [isAnnual, setIsAnnual] = useState(false);

  const backend = import.meta.env.VITE_BACK_END || ''
  const [plans, setPlans] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${backend}/api/public/plans-features`)
      .then((res) => res.json())
      .then((data) => {
        if (data.payload) {
          // transforma objeto em array para mapear
          const formattedPlans = Object.entries(data.payload).map(([name, info]: any) => ({
            name,
            description: `Plano ${name} para diferentes necessidades`,
            monthlyPrice: info.price,
            annualPrice: Math.round(info.price * 0.83), // desconto ~17%
            features: info.features,
            isPopular: name === "Premium", // destaque no frontend
          }));
          setPlans(formattedPlans);
        }
      })
      .catch((err) => console.error("Erro ao buscar planos:", err));
  }, []);
  
  return (
    <section id="pricing" className="py-24 px-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Planos que <span className="text-gradient-primary">Escalam</span>
            <br />
            com seu <span className="text-gradient-accent">Crescimento</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-8">
            Escolha o plano perfeito para sua equipe. Todos os planos incluem 7 dias grátis para testar.
          </p>

          {/* Toggle Annual/Monthly */}
          <div className="flex items-center justify-center gap-4 mb-12">
            <span className={`font-medium ${!isAnnual ? 'text-foreground' : 'text-muted-foreground'}`}>
              Mensal
            </span>
            <button
              onClick={() => setIsAnnual(!isAnnual)}
              className={`relative w-16 h-8 rounded-full transition-colors ${
                isAnnual ? 'bg-primary' : 'bg-muted'
              }`}
            >
              <div
                className={`absolute top-1 left-1 w-6 h-6 bg-white rounded-full transition-transform ${
                  isAnnual ? 'translate-x-8' : 'translate-x-0'
                }`}
              />
            </button>
            <span className={`font-medium ${isAnnual ? 'text-foreground' : 'text-muted-foreground'}`}>
              Anual
            </span>
            {isAnnual && (
              <span className="bg-accent text-accent-foreground px-3 py-1 rounded-full text-sm font-medium">
                -17% Desconto
              </span>
            )}
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((plan, index) => (
            <div
              key={plan.name}
              className={`${
                plan.isPopular ? 'pricing-card-popular' : 'pricing-card'
              } animate-scale-in`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {plan.isPopular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <div className="bg-primary text-primary-foreground px-4 py-2 rounded-full text-sm font-medium flex items-center gap-2">
                    <Star className="w-4 h-4" />
                    Mais Popular
                  </div>
                </div>
              )}

              {/* Plan Header */}
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                <p className="text-muted-foreground mb-4">{plan.description}</p>
                <div className="flex items-baseline justify-center gap-2">
                  <span className="text-4xl font-bold">
                    ${isAnnual ? plan.annualPrice : plan.monthlyPrice}
                  </span>
                  <span className="text-muted-foreground">/mês</span>
                </div>
                {isAnnual && (
                  <div className="text-sm text-muted-foreground mt-1">
                    Faturado anualmente (${(isAnnual ? plan.annualPrice : plan.monthlyPrice) * 12})
                  </div>
                )}
              </div>

              {/* Features */}
              <div className="space-y-4 mb-8">
                {plan.features.map((feature, featureIndex) => (
                  <div key={featureIndex} className="flex items-center gap-3">
                    <div className="w-5 h-5 rounded-full bg-accent/20 flex items-center justify-center">
                      <Check className="w-3 h-3 text-accent" />
                    </div>
                    <span className="text-sm">{feature}</span>
                  </div>
                ))}
              </div>

              {/* CTA Button */}
              <button
                onClick={() => window.location.href = project[0].plans.find(p => p.name === plan.name)?.checkout}
                className={`w-full ${plan.isPopular ? 'btn-hero' : 'btn-hero-outline'} group`}
              >
                {plan.isPopular ? (
                  <>
                    <Zap className="w-5 h-5 mr-2" />
                    Começar Agora
                  </>
                ) : (
                  'Escolher Plano'
                )}
              </button>


              {plan.isPopular && (
                <div className="text-center mt-4">
                  <span className="text-sm text-muted-foreground">
                    ⚡ Setup em menos de 5 minutos
                  </span>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Enterprise CTA */}
        <div className="text-center mt-16">
          <div className="card-glass p-8 max-w-3xl mx-auto">
            <h3 className="text-2xl font-bold mb-4">
              Precisa de algo <span className="text-gradient-primary">Personalizado?</span>
            </h3>
            <p className="text-muted-foreground mb-6">
              Para organizações com necessidades específicas, oferecemos planos enterprise 
              totalmente customizados com recursos avançados e suporte dedicado.
            </p>
            <button className="btn-accent">
              Falar com Especialista
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};