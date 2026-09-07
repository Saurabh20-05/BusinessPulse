// import { Link, useLocation, useNavigate } from "react-router-dom";
// import { useEffect, useState } from "react";

// import { getCurrentUser } from "../services/api";

// // const navigationLinks = [
// //   { label: "Home", path: "/" },
// //   { label: "Dashboard", path: "/dashboard" },
// // ];
// const navigationLinks = [
//   { label: "Home", path: "/" },
//   { label: "Dashboard", path: "/dashboard" },
//   { label: "Dataset", path: "/dataset" },
//   { label: "Insights", path: "/insights" },
//   { label: "Data Quality", path: "/data-quality" },
// ];

// function Navbar() {
//   const location = useLocation();
//   const navigate = useNavigate();

//   const [user, setUser] = useState(null);

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

//   const handleLogout = () => {
//     // Clear the saved login before sending the user to the login page
//     localStorage.removeItem("access_token");

//     setUser(null);

//     navigate("/login");
//   };

//   return (
//     <header className="sticky top-0 z-30 border-b border-blue-100 bg-white shadow-md">
//       <div className="w-full px-6 h-16 flex items-center justify-between">
//         {/* Logo */}

//         <Link to="/" className="text-2xl font-bold">
//           BusinessPulse
//         </Link>

//         {/* Navigation */}

//         <nav className="hidden sm:flex items-center gap-3">
//           {navigationLinks.map((link) => {
//             const isActive = location.pathname === link.path;

//             return (
//               <Link
//                 key={link.path}
//                 to={link.path}
//                 className={`px-4 py-1.5 rounded-lg text-sm font-semibold border transition-colors ${
//                   isActive
//                     ? "border-primary-500 bg-primary-50 text-primary-700"
//                     : "border-slate-400 text-slate-600 hover:bg-slate-100"
//                 }`}
//               >
//                 {link.label}
//               </Link>
//             );
//           })}
//         </nav>

//         {/* Authentication */}

//         // </div>{user ? (
//           // <div className="flex items-center gap-3">
//           //   {/* <span className="text-sm font-semibold text-slate-700">
//           //     {user.name || user.email}
//           //   </span> */}

//           //   <Link
//           //     to="/profile"
//           //     className="text-sm font-semibold text-slate-700 hover:text-primary-700"
//           //   >
//           //     {user.name || user.email}
//           //   </Link>

//           //   <button
//           //     onClick={handleLogout}
//           //     className="rounded-lg border border-slate-400 px-4 py-1.5 text-sm font-semibold text-slate-700 hover:bg-slate-200"
//           //   >
//           //     Logout
//           //   </button>
//           // </div>

//         //   <div className="flex items-center gap-4">
//         //     <Link
//         //       to="/profile"
//         //       className="flex items-center gap-1.5 text-sm font-semibold text-slate-700 hover:text-primary-700"
//         //     >
//         //       {user.name || user.email}
//         //       <span className="text-xs text-slate-400">▼</span>
//         //     </Link>

//         //     <button
//         //       onClick={handleLogout}
//         //       className="rounded-lg border border-slate-400 px-4 py-1.5 text-sm font-semibold text-slate-700 hover:bg-slate-200"
//         //     >
//         //       Logout
//         //     </button>
//         //   </div>
//         // ) : (
//         //   <Link
//         //     to="/login"
//         //     className="rounded-lg border border-slate-400 px-5 py-1.5 text-sm font-semibold text-slate-700 hover:bg-slate-200"
//         //   >
//         //     Sign In
//         //   </Link>

//         {user ? (
//   <div className="relative">
//     <Link
//       to="/profile"
//       className="flex items-center gap-2 rounded-lg px-2 py-1.5 text-sm font-semibold text-slate-700 hover:bg-slate-100"
//     >
//       <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-50 text-sm font-semibold text-primary-700">
//         {user.name?.charAt(0)?.toUpperCase() ||
//           user.email?.charAt(0)?.toUpperCase()}
//       </div>

//       <span>{user.name || user.email}</span>

//       <span className="text-xs text-slate-400">▼</span>
//     </Link>
//   </div>
// ) : (
//   <Link
//     to="/login"
//     className="rounded-lg border border-slate-400 px-5 py-1.5 text-sm font-semibold text-slate-700 hover:bg-slate-200"
//   >
//     Sign In
//   </Link>
// )}
//         )}
//       </div>
//     </header>
//   );
// }

// export default Navbar;

import { Link, useLocation, useNavigate } from "react-router-dom";
import { useEffect, useRef, useState } from "react";

import { getCurrentUser } from "../services/api";

// Navigation links shown in the navbar
// const navigationLinks = [
//   { label: "Home", path: "/" },
//   { label: "Dashboard", path: "/dashboard" },
// ];

const navigationLinks = [
  { label: "Home", path: "/" },
  { label: "Dashboard", path: "/dashboard" },
  { label: "Dataset", path: "/dataset" },
  { label: "Insights", path: "/insights" },
  { label: "Data Quality", path: "/data-quality" },
];

function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [profileOpen, setProfileOpen] = useState(false);
  const profileRef = useRef(null);

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

        {/* Previous authentication layout */}
        {/*
        {user ? (
          <div className="flex items-center gap-3">
            <Link
              to="/profile"
              className="text-sm font-semibold text-slate-700 hover:text-primary-700"
            >
              {user.name || user.email}
            </Link>

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
        */}

        {/* Previous authentication layout with dropdown indicator */}
        {/*
        {user ? (
          <div className="flex items-center gap-4">
            <Link
              to="/profile"
              className="flex items-center gap-1.5 text-sm font-semibold text-slate-700 hover:text-primary-700"
            >
              {user.name || user.email}
              <span className="text-xs text-slate-400">▼</span>
            </Link>

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
        */}

        {/* Current authentication layout */}
        {user ? (
          // <div className="relative">
          //   <Link
          //     to="/profile"
          //     className="flex items-center gap-2 rounded-lg px-2 py-1.5 text-sm font-semibold text-slate-700 hover:bg-slate-100"
          //   >
          //     {/* User avatar */}
          //     <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-50 text-sm font-semibold text-primary-700">
          //       {user.name?.charAt(0)?.toUpperCase() ||
          //         user.email?.charAt(0)?.toUpperCase()}
          //     </div>

          //     {/* User name or email */}
          //     <span>{user.name || user.email}</span>

          //     {/* Profile indicator */}
          //     <span className="text-xs text-slate-400">▼</span>
          //   </Link>
          // </div>

          <div ref={profileRef} className="relative">
            <button
              onClick={handleProfileClick}
              className="flex items-center gap-2 rounded-lg px-2 py-1.5 text-sm font-semibold text-slate-700 hover:bg-slate-100"
            >
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-50 text-sm font-semibold text-primary-700">
                {user.name?.charAt(0)?.toUpperCase() ||
                  user.email?.charAt(0)?.toUpperCase()}
              </div>

              <span>{user.name || user.email}</span>

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
                  <p className="text-sm font-semibold text-slate-800">
                    {user.name}
                  </p>

                  <p className="mt-1 text-xs text-slate-500">{user.email}</p>
                </div>

                <div className="border-t border-slate-100" />

                <Link
                  to="/profile"
                  onClick={() => setProfileOpen(false)}
                  className="block px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50"
                >
                  Profile
                </Link>

                <div className="border-t border-slate-100" />

                <button
                  onClick={handleLogout}
                  className="block w-full px-4 py-2.5 text-left text-sm font-medium text-rose-600 hover:bg-rose-50"
                >
                  Logout
                </button>
              </div>
            )}
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
