import { ArrowRight, Github, Rocket } from "lucide-react";
import { project } from "@/constants/landingpage.ts";

export const CTASection = () => {
  const { links, cta } = project[0];

  return (
    <section className="py-24 px-6 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0">
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-primary/10 via-transparent to-accent/10" />
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/20 rounded-full blur-3xl animate-pulse-glow" />
        <div
          className="absolute -bottom-40 -left-40 w-96 h-96 bg-accent/20 rounded-full blur-3xl animate-pulse-glow"
          style={{ animationDelay: "1s" }}
        />
      </div>

      <div className="max-w-4xl mx-auto text-center relative z-10">
        <div className="card-glass p-12 md:p-16">
          {/* Icon */}
          <div className="w-20 h-20 mx-auto mb-8 bg-gradient-to-br from-primary to-primary-glow rounded-2xl flex items-center justify-center animate-float">
            <Rocket className="w-10 h-10 text-primary-foreground" />
          </div>

          {/* Heading */}
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            {cta.title.split("Workflow?")[0]}
            <br />
            seu <span className="text-gradient-accent">Workflow?</span>
          </h2>

          {/* Description */}
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed">
            {cta.description}
          </p>

          {/* Benefits List */}
          <div className="flex flex-wrap justify-center gap-6 mb-12 text-sm">
            {cta.benefits.map((benefit, idx) => (
              <div key={idx} className="flex items-center gap-2">
                <div className="w-2 h-2 bg-accent rounded-full" />
                <span>{benefit}</span>
              </div>
            ))}
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href={links.app}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-hero group text-lg px-8 py-4"
            >
              <Rocket className="w-5 h-5 mr-2" />
              Começar Gratuitamente
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </a>
            <a
              href={links.github}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-hero-outline group text-lg px-8 py-4"
            >
              <Github className="w-5 h-5 mr-2" />
              Ver Código-Fonte
            </a>
          </div>

          {/* Social Proof */}
          <div className="mt-12 pt-8 border-t border-border">
            <p className="text-sm text-muted-foreground mb-4">
              {cta.socialProofTitle}
            </p>
            <div className="flex flex-wrap justify-center gap-8 opacity-60">
              {cta.companies.map((company, idx) => (
                <div key={idx} className="text-lg font-semibold">
                  {company}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
