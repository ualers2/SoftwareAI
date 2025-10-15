
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import GCL from "./pages/GCL";
import NotFound from "./pages/NotFound";
import Layout from "./components/layout";

import { AuthProvider, useAuth } from "./contexts/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";


const queryClient = new QueryClient();

// const AppRoutes = () => {
//   const { isAuthenticated } = useAuth();

//   return (
//     <BrowserRouter>
//       {isAuthenticated ? (
//         <Layout>
//           <Routes>
//             <Route path="/gitcontextlayer" element={<Index />} />
//             <Route path="/" element={<Login />} />
//             {/* <Route path="*" element={<NotFound />} /> */}
//           </Routes>
//         </Layout>
//       ) : (
//         <Routes>
//           <Route path="/" element={<Login />} />
//           <Route path="/login" element={<Login />} />

//           <Route path="*" element={<Navigate to="/" replace />} />
//         </Routes>
//       )}
//     </BrowserRouter>
//   );
// };

// const App = () => (
//   <QueryClientProvider client={queryClient}>
//     <TooltipProvider>
//       <Toaster />
//       <Sonner />
//       <AuthProvider>
//         <AppRoutes />
//       </AuthProvider>
//     </TooltipProvider>
//   </QueryClientProvider>
// );

// export default App;



const App = () => {
  return (
      <QueryClientProvider client={queryClient}>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          <AuthProvider>
            <BrowserRouter>
                <Routes>
                  {/* Rota pública, sem necessidade de autenticacao */}
                  <Route path="/" element={<Login />} />
                  <Route path="/login" element={<Login />} />

                  

                  {/* Rotas protegidas: só acessa se estiver autenticado */}
                  <Route
                    path="/gitcontextlayer"
                    element={
                      <ProtectedRoute>
                        <Layout>
                          <GCL />
                        </Layout>
                      </ProtectedRoute>
                    }
                  />

                  {/* Caso nenhuma rota seja encontrada */}
                  <Route path="*" element={<NotFound />} />
                </Routes>
            </BrowserRouter>          

          </AuthProvider>
        </TooltipProvider>
      </QueryClientProvider>
);
}
export default App;