export const project = [
{
    id: 1,
    links: {
        github: 'https://github.com/ualers2/SoftwareAI',
        app: 'https://www.softwareai.site/login',
        email: ''
    },
    cta: {
      title: "Pronto para Revolucionar seu Workflow?",
      description:
        "Junte-se a centenas de equipes que já economizam horas semanais com PR-AI. Setup em 2 minutos, resultados imediatos.",
      benefits: [
        "7 dias grátis",
        "Sem cartão de crédito",
        "Cancelamento fácil",
        "Suporte brasileiro",
      ],
      socialProofTitle: "Confiado por desenvolvedores em empresas como:",
      companies: ["Media Cuts Studio", "Employers AI", "Docshepere", "CodeLab"],
    },
    header: {
      navigation: [
        { name: "Recursos", href: "#features" },
        { name: "Preços", href: "#pricing" },
        { name: "Documentação", href: "#docs" },
        { name: "Contato", href: "#contact" },
      ],
      actions: {
        login: { label: "Entrar", href: "/login" },
        signup: { label: "Começar Grátis", href: "/signup" },
      },
    },
    plans: [
      {
        name: "Free",
        checkout: "https://www.softwareai.site/signup?plan=free"
      },
      {
        name: "Premium",
        checkout: "https://checkout.stripe.com/pay/premium123"
      },
      {
        name: "Pro",
        checkout: "https://checkout.stripe.com/pay/pro123"
      }
    ],
},

];
