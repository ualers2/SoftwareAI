// ProtectedRoute.tsx
import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { isAuthenticated } = useAuth(); // ✅ usar isAuthenticated

  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return children;
};

export default ProtectedRoute;
