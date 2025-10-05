import { useState } from "react";
import { Menu, X, Github } from "lucide-react";
import { project } from "@/constants/landingpage.ts";

export const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { header, links } = project[0];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border/50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-primary to-primary-glow rounded-lg flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-sm">AI</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gradient-primary">PR-AI</h1>
              <p className="text-xs text-muted-foreground -mt-1">by SoftwareAI</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            {header.navigation.map((item) => (
              <a
                key={item.name}
                href={item.href}
                className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
              >
                {item.name}
              </a>
            ))}
          </nav>

          {/* Desktop Actions */}
          <div className="hidden md:flex items-center gap-4">
            <a
              href={links.github}
              target="_blank"
              rel="noopener noreferrer"
              className="text-muted-foreground hover:text-primary transition-colors"
            >
              <Github className="w-5 h-5" />
            </a>
            <a
              href={header.actions.login.href}
              className="text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              {header.actions.login.label}
            </a>
            <a href={header.actions.signup.href} className="btn-hero-outline text-sm py-2 px-4">
              {header.actions.signup.label}
            </a>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden text-muted-foreground hover:text-primary"
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-border/50">
            <nav className="flex flex-col gap-4">
              {header.navigation.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors py-2"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.name}
                </a>
              ))}
              <div className="flex flex-col gap-3 pt-4 border-t border-border/50">
                <a
                  href={header.actions.login.href}
                  className="text-sm text-left text-muted-foreground hover:text-primary transition-colors"
                >
                  {header.actions.login.label}
                </a>
                <a href={header.actions.signup.href} className="btn-hero-outline text-sm py-2 px-4 w-full">
                  {header.actions.signup.label}
                </a>
              </div>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};
