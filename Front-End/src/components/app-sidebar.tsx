import { 
  Activity, 
  Bot, 
  GitPullRequest, 
  GitBranch,
  ScrollText, 
  Settings, 
  Zap,
  User,
  CreditCard,
  FileText
} from "lucide-react"
import { NavLink, useLocation } from "react-router-dom"

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  useSidebar,
} from "@/components/ui/sidebar"

import { LogOut } from "lucide-react"
import { useNavigate } from "react-router-dom"
import { useAuth } from '@/contexts/AuthContext';

const navigationItems = [
  { 
    title: "Dashboard", 
    url: "/home", 
    icon: Activity,
    description: "Visão geral do sistema"
  },
  { 
    title: "Pull Requests", 
    url: "/prs", 
    icon: GitPullRequest,
    description: "Monitoramento de PRs"
  },
  { 
    title: "Workflows", 
    url: "/workflows", 
    icon: GitBranch,
    description: "Git Workflows de Processamento"
  },
  { 
    title: "Logs", 
    url: "/logs", 
    icon: ScrollText,
    description: "Logs do sistema"
  },
  { 
    title: "Controles", 
    url: "/controls", 
    icon: Zap,
    description: "Ações e controles"
  },
  { 
    title: "Configurações", 
    url: "/settings", 
    icon: Settings,
    description: "Configurações do sistema"
  },
  { 
    title: "Conta", 
    url: "/myaccount", 
    icon: User,
    description: "Configurações da conta"
  },
  { 
    title: "Billing", 
    url: "/billing", 
    icon: CreditCard,
    description: "Configurações de faturamento"
  },  
  { 
    title: "Invoices", 
    url: "/billing/invoices", 
    icon: FileText,
    description: "Relatório de Faturas"
  },
]

// Dentro do componente AppSidebar
export function AppSidebar() {
  const { state } = useSidebar()
  const location = useLocation()
  const currentPath = location.pathname
  const isCollapsed = state === "collapsed"
  const navigate = useNavigate()
  const { logout } = useAuth();

  const isActive = (path: string) => {
    if (path === "/") return currentPath === "/"
    return currentPath.startsWith(path)
  }

  const getNavClassName = (path: string) => {
    const baseClasses = "w-full justify-start transition-all duration-200"
    return isActive(path) 
      ? `${baseClasses} bg-gradient-primary text-primary-foreground shadow-glow`
      : `${baseClasses} text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground`
  }

  const handleLogout = () => {
    logout(); 
    // navigate("/")
    window.location.reload()

  }

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="border-b border-sidebar-border">
        <div className="flex items-center gap-3 px-4 py-3">
          <Bot className="h-8 w-8 text-primary" />
          {!isCollapsed && (
            <div>
              <h2 className="text-lg font-bold text-sidebar-foreground">PR AI</h2>
              <p className="text-xs text-sidebar-foreground/60">Equipe de DevOps</p>
            </div>
          )}
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="text-sidebar-foreground/80">
            Navegação
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navigationItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <NavLink 
                      to={item.url} 
                      className={getNavClassName(item.url)}
                      end={item.url === "/"}
                    >
                      <item.icon className="h-5 w-5 shrink-0" />
                      {!isCollapsed && (
                        <div className="flex flex-col">
                          <span className="font-medium">{item.title}</span>
                          <span className="text-xs opacity-70">{item.description}</span>
                        </div>
                      )}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}

              {/* Botão de Logout */}
              <SidebarMenuItem>
                <SidebarMenuButton onClick={handleLogout}>
                  <div className="w-full justify-start transition-all duration-200 text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground flex items-center gap-2">
                    <LogOut className="h-5 w-5 shrink-0" />
                    {!isCollapsed && <span className="font-medium">Logout</span>}
                  </div>
                </SidebarMenuButton>
              </SidebarMenuItem>

            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
