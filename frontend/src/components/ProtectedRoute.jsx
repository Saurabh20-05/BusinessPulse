import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

import { getCurrentUser } from "../services/api";

function ProtectedRoute({ children }) {
  const [checking, setChecking] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    // Validate the saved token before showing the protected page
    if (!token) {
      setAuthenticated(false);
      setChecking(false);
      return;
    }

    getCurrentUser()
      .then(() => {
        setAuthenticated(true);
      })
      .catch(() => {
        // Clear an expired or invalid token
        localStorage.removeItem("access_token");
        setAuthenticated(false);
      })
      .finally(() => {
        setChecking(false);
      });
  }, []);

  if (checking) {
    return (
      <div className="min-h-[calc(100vh-6rem)] flex items-center justify-center">
        <p className="text-lg text-slate-600">Checking authentication...</p>
      </div>
    );
  }

  if (!authenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export default ProtectedRoute;
