import { Link, useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

import { getCurrentUser } from "../services/api";

const navigationLinks = [
  { label: "Home", path: "/" },
  { label: "Dashboard", path: "/dashboard" },
];

function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();

  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    // Check for a saved token before loading the user
    if (!token) {
      setUser(null);
      return;
    }

    getCurrentUser()
      .then((data) => {
        setUser(data);
      })
      .catch(() => {
        // Remove the token if it is no longer valid
        localStorage.removeItem("access_token");
        setUser(null);
      });
  }, [location.pathname]);

  const handleLogout = () => {
    // Clear the saved login before sending the user to the login page
    localStorage.removeItem("access_token");

    setUser(null);

    navigate("/login");
  };

  return (
    <header className="sticky top-0 z-30 border-b border-blue-100 bg-white shadow-md">
      <div className="w-full px-6 h-16 flex items-center justify-between">
        {/* Logo */}

        <Link to="/" className="text-2xl font-bold">
          BusinessPulse
        </Link>

        {/* Navigation */}

        <nav className="hidden sm:flex items-center gap-3">
          {navigationLinks.map((link) => {
            const isActive = location.pathname === link.path;

            return (
              <Link
                key={link.path}
                to={link.path}
                className={`px-4 py-1.5 rounded-lg text-sm font-semibold border transition-colors ${
                  isActive
                    ? "border-primary-500 bg-primary-50 text-primary-700"
                    : "border-slate-400 text-slate-600 hover:bg-slate-100"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        {/* Authentication */}

        {user ? (
          <div className="flex items-center gap-3">
            <span className="text-sm font-semibold text-slate-700">
              {user.name || user.email}
            </span>

            <button
              onClick={handleLogout}
              className="rounded-lg border border-slate-400 px-4 py-1.5 text-sm font-semibold text-slate-700 hover:bg-slate-200"
            >
              Logout
            </button>
          </div>
        ) : (
          <Link
            to="/login"
            className="rounded-lg border border-slate-400 px-5 py-1.5 text-sm font-semibold text-slate-700 hover:bg-slate-200"
          >
            Sign In
          </Link>
        )}
      </div>
    </header>
  );
}

export default Navbar;
