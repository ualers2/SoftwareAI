
import { Toaster } from "./components/ui/toaster";
import { Toaster as Sonner } from "./components/ui/sonner";
import { TooltipProvider } from "./components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/layout";
import Dashboard from "./pages/Dashboard";
import PullRequests from "./pages/PullRequests";
import Logs from "./pages/Logs";
import Controls from "./pages/Controls";
import Settings from "./pages/Settings";
import NotFound from "./pages/NotFound";
import Workflows from "./pages/Workflows"; 
import MyAccount from "./pages/MyAccount"; 
import BillingPage from "./pages/Billing"; 
import InvoicesPage from "./pages/Invoices"; 
import Index from "./pages/Landingpage";

import SignupCheckout from "./pages/SignupCheckout";
import CheckoutSuccess from "./pages/CheckoutSuccess";
import CheckoutError from "./pages/CheckoutError";

import CommitMessages from "./pages/CommitMessages";
import AgentTasks from "./pages/AgentTasks";

import Chat from "./pages/Chat";
import Login from "./pages/Login";

import { AuthProvider, useAuth } from "./contexts/AuthContext";
import type { ColorScheme } from "./hooks/useColorScheme";
import { useColorScheme } from "./hooks/useColorScheme";
import { useCallback } from "react";

const queryClient = new QueryClient();

const AppRoutes = () => {
  const { isAuthenticated } = useAuth();
  const { scheme, setScheme } = useColorScheme();
  const handleThemeChange = useCallback(
    (value: "light" | "dark") => {
      setScheme(value);
    },
    [setScheme]
  );

  return (
    <BrowserRouter>
      {isAuthenticated ? (
        <Layout>
          <Routes>
            <Route path="/home" element={<Dashboard />} />
            <Route path="/chat" element={<Chat scheme={scheme} handleThemeChange={handleThemeChange}/>} />

            <Route path="/tasks" element={<AgentTasks />} />
            <Route path="/workflows" element={<Workflows />} />
            <Route path="/prs" element={<PullRequests />} />
            <Route path="/commits" element={<CommitMessages />} />

            <Route path="/logs" element={<Logs />} />
            <Route path="/controls" element={<Controls />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/myaccount" element={<MyAccount />} />
            <Route path="/billing" element={<BillingPage />} />
            <Route path="/billing/invoices" element={<InvoicesPage />} />
          
            <Route path="*" element={<NotFound />} />
          
          
          </Routes>
        </Layout>
      ) : (
        <Routes>

          <Route path="/" element={<Index />} />
          <Route path="/login" element={<Login />} />


          <Route path="/checkout" element={<SignupCheckout />} />
          <Route path="/checkout/sucess" element={<CheckoutSuccess />} />
          <Route path="/checkout/cancel" element={<CheckoutError />} />

          <Route path="*" element={<Navigate to="/" replace />} />

        </Routes>
      )}
    </BrowserRouter>
  );
};

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
