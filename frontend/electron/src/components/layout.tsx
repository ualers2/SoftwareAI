import { ReactNode } from "react"
import { SidebarProvider, SidebarTrigger, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"

interface LayoutProps {
  children: ReactNode
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full bg-gradient-hero">
        <AppSidebar />
        <SidebarInset className="flex-1">
          {/* Header with sidebar trigger */}
          <header className="sticky top-0 z-10 flex h-16 shrink-0 items-center gap-2 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 px-4">
            <SidebarTrigger className="text-foreground" />
            {/* <div className="flex items-center gap-2">
              <div className="h-6 w-px bg-border" />
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-success animate-pulse" />
                <span className="text-sm text-muted-foreground">Sistema Online</span>
              </div>
            </div> */}
          </header>
          {/* Main content */}
          <main className="flex-1 p-6">
            {children}
          </main>
        </SidebarInset>
      </div>
    </SidebarProvider>
  )
}

export default Layout