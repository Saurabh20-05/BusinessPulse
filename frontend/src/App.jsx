// import { useEffect } from "react";
// import { Routes, Route, useLocation } from "react-router-dom";

// import Navbar from "./components/Navbar";
// import Footer from "./components/Footer";

// import ProtectedRoute from "./components/ProtectedRoute";
// import PublicRoute from "./components/PublicRoute";

// import Home from "./pages/Home";
// import Dashboard from "./pages/Dashboard";
// import Login from "./pages/Login";
// import Signup from "./pages/Signup";

// import Dataset from "./pages/Dataset";

// import Insights from "./pages/Insights";

// import DataQuality from "./pages/DataQuality";

// import Profile from "./pages/Profile";

// function ScrollToTop() {
//   const { pathname, search } = useLocation();

//   useEffect(() => {
//     window.scrollTo(0, 0);
//   }, [pathname, search]);

//   return null;
// }

// function App() {
//   return (
//     <div className="min-h-screen flex flex-col">
//       <Navbar />
//       <ScrollToTop />

//       <main className="flex-1">
//         <Routes>
//           <Route path="/" element={<Home />} />

//           <Route
//             path="/login"
//             element={
//               <PublicRoute>
//                 <Login />
//               </PublicRoute>
//             }
//           />

//           <Route
//             path="/signup"
//             element={
//               <PublicRoute>
//                 <Signup />
//               </PublicRoute>
//             }
//           />

//           <Route
//             path="/dashboard"
//             element={
//               <ProtectedRoute>
//                 <Dashboard />
//               </ProtectedRoute>
//             }
//           />

//           <Route path="/dataset" element={<Dataset />} />

//           <Route path="/insights" element={<Insights />} />

//           <Route
//             path="/data-quality"
//             element={
//               <ProtectedRoute>
//                 <DataQuality />
//               </ProtectedRoute>
//             }
//           />

//           <Route
//             path="/profile"
//             element={
//               <ProtectedRoute>
//                 <Profile />
//               </ProtectedRoute>
//             }
//           />
//         </Routes>
//       </main>

//       <Footer />
//     </div>
//   );
// }

// export default App;




import { useEffect } from "react";
import { Routes, Route, useLocation } from "react-router-dom";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import ProtectedRoute from "./components/ProtectedRoute";
import PublicRoute from "./components/PublicRoute";

import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Signup from "./pages/Signup";

import Dataset from "./pages/Dataset";

import Insights from "./pages/Insights";

import DataQuality from "./pages/DataQuality";

import Profile from "./pages/Profile";

import AIAnalytics from "./pages/AIAnalytics";

function ScrollToTop() {
  const { pathname, search } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname, search]);

  return null;
}

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <ScrollToTop />

      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Home />} />

          <Route
            path="/login"
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            }
          />

          <Route
            path="/signup"
            element={
              <PublicRoute>
                <Signup />
              </PublicRoute>
            }
          />

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route path="/dataset" element={<Dataset />} />

          <Route path="/insights" element={<Insights />} />

          <Route
            path="/data-quality"
            element={
              <ProtectedRoute>
                <DataQuality />
              </ProtectedRoute>
            }
          />

          <Route
            path="/ai-analytics"
            element={
              <ProtectedRoute>
                <AIAnalytics />
              </ProtectedRoute>
            }
          />

          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>

      <Footer />
    </div>
  );
}

export default App;