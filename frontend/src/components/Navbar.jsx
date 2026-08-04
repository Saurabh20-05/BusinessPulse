
import { Link, useLocation } from "react-router-dom";




const navigationLinks = [
  { label: "Home", path: "/" },
  { label: "Dashboard", path: "/dashboard" },
];




function Navbar() {
  
  
  
  const location = useLocation();

  return (
    
    
    <header className="sticky top-0 z-30 border-b border-blue-100 bg-white shadow-md">
      
      
      <div className="w-full px-12 h-24 flex items-center justify-between">

        
        
        <Link to="/" className="text-4xl font-bold">
          BusinessPulse
        </Link>

        


        <nav className="hidden sm:flex items-center gap-10">
          {navigationLinks.map((link) => {
            const isActive = location.pathname === link.path;
            
            return (
              
              <Link
                key={link.path}
                to={link.path}
                className={`px-6 py-3 rounded-lg text-lg font-semibold border transition-colors ${
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



        <button className="rounded-xl border border-slate-400 px-8 py-3 text-lg font-semibold text-slate-700 hover:bg-slate-200">
          Sign In


        </button>

      </div>
    </header>
  );
}

export default Navbar;