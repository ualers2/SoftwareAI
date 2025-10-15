// webproject\src/components\LoginForm.tsx
import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Mail, Lock, LogIn, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [access_token_fallback, setaccess_token_fallback] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();
  const { login } = useAuth();

  const backendUrl = import.meta.env.VITE_BACK_END;

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) return;
    setIsLoading(true);
    setError(null);
    const access_token = localStorage.getItem("access_token");

    try {
      const response = await fetch(`${backendUrl}/api/login?email=${email}&password=${password}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token}`
        },
      });

      const result = await response.json();
      console.log('login response status', response.status, result);

      if (!response.ok) {
        throw new Error(result.message || 'Erro no login');
      }

      const token = result.acess_token;
      if (!token) throw new Error('Resposta sem access_token');

      localStorage.setItem('isAuthenticated', 'true');
      const formattedTime = new Date().toLocaleString('en-US', {
        hour: 'numeric', minute: 'numeric', hour12: true,
        day: '2-digit', month: 'short', year: 'numeric'
      });
      localStorage.setItem('login_time', formattedTime);
      localStorage.setItem('acess_token', token);
      localStorage.setItem('access_token', token);
      localStorage.setItem('user_email', email); 
      localStorage.setItem('user_senha', email); 
      setaccess_token_fallback(token);

      console.log('Token access_token:', token);
      console.log('Token access_token_fallback:', token);

      login(token); 
      navigate(`/home`);

    } catch (err: any) {
      setError(err.message || 'Erro no login');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-foreground">PR AI</h1>
          <p className="text-muted-foreground">
            Bem-vindo de volta! Faça login para continuar
          </p>
        </div>
        
        <Card className="shadow-lg">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">Login</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-muted-foreground flex items-center" htmlFor="email">
                  <Mail className="mr-2 h-4 w-4" /> Email
                </label>
                <Input 
                  id="email" 
                  type="email" 
                  placeholder="seu@email.com" 
                  value={email} 
                  onChange={e => setEmail(e.target.value)} 
                  required 
                  disabled={isLoading} 
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-muted-foreground flex items-center" htmlFor="password">
                  <Lock className="mr-2 h-4 w-4" /> Senha
                </label>
                <Input 
                  id="password" 
                  type="password" 
                  placeholder="Sua senha" 
                  value={password} 
                  onChange={e => setPassword(e.target.value)} 
                  required 
                  disabled={isLoading} 
                />
              </div>

              {error && (
                <p className="text-sm text-destructive-foreground bg-destructive p-2 rounded-md text-center">{error}</p>
              )}

              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <LogIn className="mr-2 h-4 w-4" />
                )}
                Entrar
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default LoginForm;
