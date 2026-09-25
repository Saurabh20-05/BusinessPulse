// import { Link, useLocation, useNavigate } from "react-router-dom";
// import { useEffect, useRef, useState } from "react";
// import { useTranslation } from "react-i18next";

// import { getCurrentUser } from "../services/api";

// const navigationLinks = [
//   { key: "home", path: "/" },
//   { key: "dashboard", path: "/dashboard" },
//   { key: "dataset", path: "/dataset" },
//   { key: "insights", path: "/insights" },
//   { key: "dataQuality", path: "/data-quality" },
// ];

// function Navbar() {
//   const location = useLocation();
//   const navigate = useNavigate();
//   const { t, i18n } = useTranslation();

//   const [user, setUser] = useState(null);
//   const [profileOpen, setProfileOpen] = useState(false);

//   const profileRef = useRef(null);

//   useEffect(() => {
//     const token = localStorage.getItem("access_token");

//     // Check for a saved token before loading the user
//     if (!token) {
//       setUser(null);
//       return;
//     }

//     getCurrentUser()
//       .then((data) => {
//         setUser(data);
//       })
//       .catch(() => {
//         // Remove the token if it is no longer valid
//         localStorage.removeItem("access_token");
//         setUser(null);
//       });
//   }, [location.pathname]);

//   useEffect(() => {
//     const handleClickOutside = (event) => {
//       if (!profileRef.current?.contains(event.target)) {
//         setProfileOpen(false);
//       }
//     };

//     if (profileOpen) {
//       document.addEventListener("click", handleClickOutside);
//     }

//     return () => {
//       document.removeEventListener("click", handleClickOutside);
//     };
//   }, [profileOpen]);

//   const handleProfileClick = () => {
//     setProfileOpen((open) => !open);
//   };

//   const handleLogout = () => {
//     // Clear the saved login before sending the user to the login page
//     localStorage.removeItem("access_token");

//     setUser(null);
//     setProfileOpen(false);

//     navigate("/login");
//   };

//   return (
//     <header className="sticky top-0 z-30 border-b border-slate-200 bg-white shadow-sm">
//       <div className="grid h-16 w-full grid-cols-[1fr_auto_1fr] items-center px-6">
//         {/* Logo */}
//         <div className="flex items-center">
//           <Link
//             to="/"
//             className="text-2xl font-bold tracking-tight text-slate-800"
//           >
//             BusinessPulse
//           </Link>
//         </div>

//         {/* Navigation */}
//         <nav className="hidden items-center justify-center gap-2 sm:flex">
//           {navigationLinks.map((link) => {
//             const isActive =
//               link.path === "/"
//                 ? location.pathname === "/"
//                 : location.pathname === link.path ||
//                   location.pathname.startsWith(`${link.path}/`);

//             return (
//               <Link
//                 key={link.path}
//                 to={link.path}
//                 className={`rounded-lg border px-4 py-2 text-sm font-semibold transition-colors ${
//                   isActive
//                     ? "border-primary-500 bg-primary-50 text-primary-700"
//                     : "border-slate-300 bg-white text-slate-600 hover:bg-slate-50 hover:text-slate-800"
//                 }`}
//               >
//                 {t(link.key)}
//               </Link>
//             );
//           })}
//         </nav>

//         {/* Language + Profile */}
//         <div className="flex items-center justify-end gap-3">
//           <select
//             value={i18n.language}
//             onChange={(e) => i18n.changeLanguage(e.target.value)}
//             className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-600 outline-none transition focus:border-primary-400"
//           >
//             <option value="en">English</option>
//             <option value="hi">Hindi</option>
//             <option value="es">Spanish</option>
//             <option value="fr">French</option>
//             <option value="de">German</option>
//           </select>

//           {user ? (
//             <div ref={profileRef} className="relative">
//               <button
//                 type="button"
//                 onClick={handleProfileClick}
//                 className="flex items-center gap-2 rounded-lg px-2 py-1.5 text-sm font-semibold text-slate-700 transition-colors hover:bg-slate-100"
//               >
//                 <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-50 text-sm font-semibold text-primary-700">
//                   {user.name?.charAt(0)?.toUpperCase() ||
//                     user.email?.charAt(0)?.toUpperCase()}
//                 </div>

//                 <span className="max-w-28 truncate">
//                   {user.name || user.email}
//                 </span>

//                 <span
//                   className={`text-xs text-slate-400 transition-transform ${
//                     profileOpen ? "rotate-180" : ""
//                   }`}
//                 >
//                   ▼
//                 </span>
//               </button>

//               {profileOpen && (
//                 <div className="absolute right-0 top-full mt-2 w-64 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-lg">
//                   <div className="px-4 py-3">
//                     <p className="truncate text-sm font-semibold text-slate-800">
//                       {user.name}
//                     </p>

//                     <p className="mt-1 truncate text-xs text-slate-500">
//                       {user.email}
//                     </p>
//                   </div>

//                   <div className="border-t border-slate-100" />

//                   <Link
//                     to="/profile"
//                     onClick={() => setProfileOpen(false)}
//                     className="block px-4 py-2.5 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50"
//                   >
//                     {t("profile")}
//                   </Link>

//                   <div className="border-t border-slate-100" />

//                   <button
//                     type="button"
//                     onClick={handleLogout}
//                     className="block w-full px-4 py-2.5 text-left text-sm font-medium text-rose-600 transition-colors hover:bg-rose-50"
//                   >
//                     {t("logout")}
//                   </button>
//                 </div>
//               )}
//             </div>
//           ) : (
//             <Link
//               to="/login"
//               className="rounded-lg border border-slate-300 bg-white px-5 py-2 text-sm font-semibold text-slate-600 transition-colors hover:bg-slate-50 hover:text-slate-800"
//             >
//               {t("login")}
//             </Link>
//           )}
//         </div>
//       </div>
//     </header>
//   );
// }

// export default Navbar;

import { Link, useLocation, useNavigate } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { getCurrentUser } from "../services/api";

const navigationLinks = [
  { key: "home", path: "/" },
  { key: "dashboard", path: "/dashboard" },
  { key: "dataset", path: "/dataset" },
  { key: "insights", path: "/insights" },
  { key: "dataQuality", path: "/data-quality" },
  { key: "aiAnalytics", path: "/ai-analytics" },
];

function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();

  const [user, setUser] = useState(null);
  const [profileOpen, setProfileOpen] = useState(false);

  const profileRef = useRef(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setUser(null);
      return;
    }

    getCurrentUser()
      .then((data) => {
        setUser(data);
      })
      .catch(() => {
        localStorage.removeItem("access_token");
        setUser(null);
      });
  }, [location.pathname]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (!profileRef.current?.contains(event.target)) {
        setProfileOpen(false);
      }
    };

    if (profileOpen) {
      document.addEventListener("click", handleClickOutside);
    }

    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, [profileOpen]);

  const handleProfileClick = () => {
    setProfileOpen((open) => !open);
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");

    setUser(null);
    setProfileOpen(false);

    navigate("/login");
  };

  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white shadow-sm">
      <div className="grid h-16 w-full grid-cols-[1fr_auto_1fr] items-center px-6">
        <div className="flex items-center">
          <Link
            to="/"
            className="text-2xl font-bold tracking-tight text-slate-800"
          >
            BusinessPulse
          </Link>
        </div>

        <nav className="hidden items-center justify-center gap-2 sm:flex">
          {navigationLinks.map((link) => {
            const isActive =
              link.path === "/"
                ? location.pathname === "/"
                : location.pathname === link.path ||
                  location.pathname.startsWith(`${link.path}/`);

            return (
              <Link
                key={link.path}
                to={link.path}
                className={`rounded-lg border px-4 py-2 text-sm font-semibold transition-colors ${
                  isActive
                    ? "border-primary-500 bg-primary-50 text-primary-700"
                    : "border-slate-300 bg-white text-slate-600 hover:bg-slate-50 hover:text-slate-800"
                }`}
              >
                {t(link.key)}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center justify-end gap-3">
          <select
            value={i18n.language}
            onChange={(e) => i18n.changeLanguage(e.target.value)}
            className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-600 outline-none transition focus:border-primary-400"
          >
            <option value="en">English</option>
            <option value="hi">Hindi</option>
            <option value="es">Spanish</option>
            <option value="fr">French</option>
            <option value="de">German</option>
          </select>

          {user ? (
            <div ref={profileRef} className="relative">
              <button
                type="button"
                onClick={handleProfileClick}
                className="flex items-center gap-2 rounded-lg px-2 py-1.5 text-sm font-semibold text-slate-700 transition-colors hover:bg-slate-100"
              >
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-50 text-sm font-semibold text-primary-700">
                  {user.name?.charAt(0)?.toUpperCase() ||
                    user.email?.charAt(0)?.toUpperCase()}
                </div>

                <span className="max-w-28 truncate">
                  {user.name || user.email}
                </span>

                <span
                  className={`text-xs text-slate-400 transition-transform ${
                    profileOpen ? "rotate-180" : ""
                  }`}
                >
                  ▼
                </span>
              </button>

              {profileOpen && (
                <div className="absolute right-0 top-full mt-2 w-64 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-lg">
                  <div className="px-4 py-3">
                    <p className="truncate text-sm font-semibold text-slate-800">
                      {user.name}
                    </p>

                    <p className="mt-1 truncate text-xs text-slate-500">
                      {user.email}
                    </p>
                  </div>

                  <div className="border-t border-slate-100" />

                  <Link
                    to="/profile"
                    onClick={() => setProfileOpen(false)}
                    className="block px-4 py-2.5 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50"
                  >
                    {t("profile")}
                  </Link>

                  <div className="border-t border-slate-100" />

                  <button
                    type="button"
                    onClick={handleLogout}
                    className="block w-full px-4 py-2.5 text-left text-sm font-medium text-rose-600 transition-colors hover:bg-rose-50"
                  >
                    {t("logout")}
                  </button>
                </div>
              )}
            </div>
          ) : (
            <Link
              to="/login"
              className="rounded-lg border border-slate-300 bg-white px-5 py-2 text-sm font-semibold text-slate-600 transition-colors hover:bg-slate-50 hover:text-slate-800"
            >
              {t("login")}
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}

export default Navbar;