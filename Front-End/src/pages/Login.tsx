// webproject\src/components\LoginForm.tsx
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Mail, Lock, LogIn, UserPlus, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const [access_token_fallback, setaccess_token_fallback] = useState('');
  // Melhoria de UX: estados para loading e erro
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();
  const { login } = useAuth();

  const backendUrl = import.meta.env.VITE_BACK_END;
  const access_token = localStorage.getItem("access_token")
  console.log('Token access_token:', access_token)
  console.log('Token access_token_fallback:', access_token_fallback)
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) return;
    setIsLoading(true);
    setError(null);

    try {

      const response = await fetch(`${backendUrl}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-TOKEN': `${access_token_fallback}`
         },
        body: JSON.stringify({ email, password }),
      });
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.message || 'Erro no login');
      }
      
      const formattedTime = new Date().toLocaleString('en-US', {
        hour: 'numeric', minute: 'numeric', hour12: true,
        day: '2-digit', month: 'short', year: 'numeric'
      });
      // Armazena dados de sessão
      localStorage.setItem('isAuthenticated', 'true');
      localStorage.setItem('login_time', formattedTime);
      setaccess_token_fallback(result.access_token)
      localStorage.setItem('access_token', access_token_fallback);
      login(result.access_token);
      navigate(`/home`);

    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError('As senhas não coincidem.');
      return;
    }
    
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${backendUrl}/api/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const result = await response.json();
      localStorage.setItem('user_email', email);
      localStorage.setItem('user_senha', password);
      setaccess_token_fallback(result.access_token)
      localStorage.setItem('access_token', access_token_fallback);
      if (!response.ok) {
        throw new Error(result.message || 'Erro no registro');
      }
      
      // Sucesso! Volta para a tela de login.
      setIsRegistering(false);
      // Você pode adicionar uma notificação de sucesso aqui (usando um 'toast', por exemplo)

    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleMode = () => {
    setIsRegistering(!isRegistering);
    setError(null); // Limpa erros ao trocar de modo
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-foreground">PR AI</h1>
          <p className="text-muted-foreground">
            {isRegistering ? "Crie sua conta para começar" : "Bem-vindo de volta! Faça login para continuar"}
          </p>
        </div>
        
        <Card className="shadow-lg">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">
              {isRegistering ? 'Criar Conta' : 'Login'}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={isRegistering ? handleRegister : handleLogin} className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-muted-foreground flex items-center" htmlFor="email">
                  <Mail className="mr-2 h-4 w-4" /> Email
                </label>
                <Input id="email" type="email" placeholder="seu@email.com" value={email} onChange={e => setEmail(e.target.value)} required disabled={isLoading} />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-muted-foreground flex items-center" htmlFor="password">
                  <Lock className="mr-2 h-4 w-4" /> Senha
                </label>
                <Input id="password" type="password" placeholder="Sua senha" value={password} onChange={e => setPassword(e.target.value)} required disabled={isLoading} />
              </div>

              {isRegistering && (
                <div className="space-y-2">
                   <label className="text-sm font-medium text-muted-foreground flex items-center" htmlFor="confirmPassword">
                    <Lock className="mr-2 h-4 w-4" /> Confirmar Senha
                  </label>
                  <Input id="confirmPassword" type="password" placeholder="Confirme sua senha" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} required disabled={isLoading} />
                </div>
              )}

              {error && (
                <p className="text-sm text-destructive-foreground bg-destructive p-2 rounded-md text-center">{error}</p>
              )}

              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  isRegistering ? <UserPlus className="mr-2 h-4 w-4" /> : <LogIn className="mr-2 h-4 w-4" />
                )}
                {isRegistering ? 'Registrar' : 'Entrar'}
              </Button>
            </form>

            <p className="text-center text-sm text-muted-foreground mt-6">
              {isRegistering ? 'Já tem uma conta?' : 'Não tem uma conta?'}
              <Button variant="link" onClick={toggleMode} className="font-semibold text-primary">
                {isRegistering ? 'Fazer login' : 'Criar conta'}
              </Button>
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default LoginForm;