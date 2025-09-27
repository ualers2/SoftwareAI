import { 
  Bot, 
  Clock, 
  FileText, 
  GitBranch, 
  LineChart, 
  Shield, 
  Webhook, 
  Zap 
} from "lucide-react";

export const FeaturesSection = () => {
  const features = [
    {
      icon: Bot,
      title: "IA Avançada",
      description: "Powered by GPT-5 otimizado para análise de código e geração de documentação técnica precisa.",
      gradient: "from-purple-500 to-blue-500"
    },
    {
      icon: Clock,
      title: "90% Economia de Tempo",
      description: "Automatize completamente a criação de descrições de PRs. Foque no que realmente importa: o código.",
      gradient: "from-green-500 to-teal-500"
    },
    {
      icon: GitBranch,
      title: "Integração GitHub",
      description: "Setup em 2 minutos via webhook. Funciona automaticamente com qualquer repositório público ou privado.",
      gradient: "from-orange-500 to-red-500"
    },
    {
      icon: FileText,
      title: "Templates Inteligentes",
      description: "Descrições estruturadas seguindo as melhores práticas de documentação de engenharia de software.",
      gradient: "from-blue-500 to-indigo-500"
    },
    {
      icon: LineChart,
      title: "Analytics & Insights",
      description: "Dashboard completo com métricas de produtividade, qualidade de código e performance da equipe.",
      gradient: "from-pink-500 to-purple-500"
    },
    {
      icon: Shield,
      title: "Segurança Enterprise",
      description: "JWT authentication, logs de auditoria completos e conformidade com padrões de segurança.",
      gradient: "from-cyan-500 to-blue-500"
    },
    {
      icon: Webhook,
      title: "Webhooks Customizados",
      description: "Integre com Slack, Discord, Teams ou qualquer ferramenta via webhooks personalizáveis.",
      gradient: "from-yellow-500 to-orange-500"
    },
    {
      icon: Zap,
      title: "Processamento Instantâneo",
      description: "Chunking inteligente para PRs de qualquer tamanho. Processamento em segundos, não minutos.",
      gradient: "from-emerald-500 to-green-500"
    }
  ];

  return (
    <section id="features" className="py-24 px-6 relative">
      {/* Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 -left-10 w-72 h-72 bg-primary/5 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 -right-10 w-96 h-96 bg-accent/5 rounded-full blur-3xl" />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Recursos que <span className="text-gradient-primary">Aceleram</span>
            <br />
            sua <span className="text-gradient-accent">Produtividade</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            PR-AI não é apenas outro bot. É a primeira equipe de IA verdadeiramente funcional, 
            projetada para integrar perfeitamente ao seu workflow existente.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className="card-glass p-6 group hover:scale-105 transition-all duration-500 animate-fade-in-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Icon */}
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                <feature.icon className="w-6 h-6 text-white" />
              </div>

              {/* Content */}
              <h3 className="text-lg font-semibold mb-3 group-hover:text-primary transition-colors">
                {feature.title}
              </h3>
              <p className="text-muted-foreground text-sm leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Stats Section */}
        <div className="mt-24 card-glass p-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div className="group">
              <div className="text-3xl md:text-4xl font-bold text-gradient-primary mb-2">90%</div>
              <div className="text-muted-foreground text-sm font-medium">Menos Tempo</div>
              <div className="text-muted-foreground text-xs">na documentação</div>
            </div>
            <div className="group">
              <div className="text-3xl md:text-4xl font-bold text-gradient-accent mb-2">2min</div>
              <div className="text-muted-foreground text-sm font-medium">Setup</div>
              <div className="text-muted-foreground text-xs">integração completa</div>
            </div>
            <div className="group">
              <div className="text-3xl md:text-4xl font-bold text-gradient-primary mb-2">24/7</div>
              <div className="text-muted-foreground text-sm font-medium">Automação</div>
              <div className="text-muted-foreground text-xs">sem intervenção</div>
            </div>
            <div className="group">
              <div className="text-3xl md:text-4xl font-bold text-gradient-accent mb-2">100%</div>
              <div className="text-muted-foreground text-sm font-medium">Consistência</div>
              <div className="text-muted-foreground text-xs">na documentação</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};