
import { Navigate } from 'react-router';
import { useAuth } from '../../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const { token } = useAuth();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}