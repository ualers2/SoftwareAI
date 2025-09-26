// src/contexts/AuthContext.tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';

interface AuthContextType {
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  // Aqui usamos localStorage para persistir o token; você pode adaptar conforme precisar
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => {
    return !!localStorage.getItem('auth_token');
  });

  function login(token: string) {
    localStorage.setItem('auth_token', token);
    setIsAuthenticated(true);
  }

  function logout() {
    localStorage.removeItem('auth_token');
    setIsAuthenticated(false);
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth deve ser usado dentro de AuthProvider');
  return ctx;
}
