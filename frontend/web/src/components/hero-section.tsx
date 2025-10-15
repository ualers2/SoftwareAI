import { ArrowRight, Github, Zap } from "lucide-react";
import heroImage from "@/assets/hero-image.jpg";
import { project } from "@/constants/landingpage";

export const HeroSection = () => {
  const { github, app } = project[0].links;



  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0 z-0">
        <img 
          src={heroImage} 
          alt="PR-AI Hero Background" 
          className="w-full h-full object-cover opacity-20"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-background via-background/95 to-background-secondary/90" />
      </div>
      
      {/* Floating Elements */}
      <div className="absolute inset-0 z-10">
        <div className="animate-float absolute top-20 left-10 w-16 h-16 bg-primary/20 rounded-full blur-xl" />
        <div className="animate-float absolute top-40 right-20 w-24 h-24 bg-accent/20 rounded-full blur-xl" style={{ animationDelay: '2s' }} />
        <div className="animate-float absolute bottom-32 left-1/4 w-20 h-20 bg-primary/15 rounded-full blur-xl" style={{ animationDelay: '4s' }} />
      </div>

      {/* Main Content */}
      <div className="relative z-20 max-w-7xl mx-auto px-6 text-center">
        <div className="animate-fade-in-up">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-primary/10 border border-primary/30 rounded-full px-4 py-2 mb-8">
            <Zap className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">Primeiro Protótipo Funcional</span>
          </div>

          {/* Main Heading */}
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            <span className="text-gradient-primary">PR-AI</span>
            <br />
            <span className="text-foreground">Automatize sua</span>
            <br />
            <span className="text-gradient-accent">Documentação</span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-3xl mx-auto leading-relaxed">
            A primeira equipe de IA funcional do <strong className="text-primary">SoftwareAI</strong>. 
            Gere descrições de Pull Requests profissionais automaticamente e economize 90% do seu tempo.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <a href={app} target="_blank" rel="noopener noreferrer" className="btn-hero group">
              Começar Gratuitamente
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </a>
            <a href={github} target="_blank" rel="noopener noreferrer" className="btn-hero-outline group flex items-center">
              <Github className="w-5 h-5 mr-2" />
              Ver no GitHub
            </a>
          </div>

          {/* Trust Indicators */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="flex items-center justify-center gap-3">
              <div className="feature-icon">
                <Zap className="w-6 h-6" />
              </div>
              <div className="text-left">
                <div className="font-semibold">90% Economia</div>
                <div className="text-sm text-muted-foreground">de tempo na documentação</div>
              </div>
            </div>
            <div className="flex items-center justify-center gap-3">
              <div className="feature-icon">
                <Github className="w-6 h-6" />
              </div>
              <div className="text-left">
                <div className="font-semibold">GitHub Integration</div>
                <div className="text-sm text-muted-foreground">Webhook automático</div>
              </div>
            </div>
            <div className="flex items-center justify-center gap-3">
              <div className="feature-icon">
                <ArrowRight className="w-6 h-6" />
              </div>
              <div className="text-left">
                <div className="font-semibold">IA Avançada</div>
                <div className="text-sm text-muted-foreground">GPT-5 otimizado</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-primary/50 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-primary rounded-full mt-2 animate-pulse" />
        </div>
      </div>
    </section>
  );
};