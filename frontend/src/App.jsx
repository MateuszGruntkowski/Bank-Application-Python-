import { useState, useEffect } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import api from "./api";
import config from "./config";
import Sidebar from "./components/Sidebar";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import HistoryPage from "./pages/HistoryPage";
import TransfersPage from "./pages/TransfersPage";
import ATMPage from "./pages/ATMPage";
import LoansPage from "./pages/LoansPage";
import SavingsPage from "./pages/SavingsPage";
import StandingOrdersPage from "./pages/StandingOrdersPage";
import NotificationsPage from "./pages/NotificationsPage";
import ProfilePage from "./pages/ProfilePage";
import AdminPage from "./pages/AdminPage";

function ProtectedRoute({ children, user }) {
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

function AdminRoute({ children, user }) {
  if (!user) return <Navigate to="/login" replace />;
  if (!user.is_admin) return <Navigate to="/" replace />;
  return children;
}

export default function App() {
  const [user, setUser] = useState(api.getUser());

  useEffect(() => {
    document.title = config.bankName;
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    api.clearToken();
    setUser(null);
  };

  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar user={user} onLogout={handleLogout} />
      <main className="flex-1 overflow-y-auto p-6 lg:p-8">
        <Routes>
          <Route path="/" element={<ProtectedRoute user={user}><DashboardPage /></ProtectedRoute>} />
          <Route path="/history" element={<ProtectedRoute user={user}><HistoryPage /></ProtectedRoute>} />
          <Route path="/transfers" element={<ProtectedRoute user={user}><TransfersPage /></ProtectedRoute>} />
          <Route path="/atm" element={<ProtectedRoute user={user}><ATMPage /></ProtectedRoute>} />
          <Route path="/loans" element={<ProtectedRoute user={user}><LoansPage /></ProtectedRoute>} />
          <Route path="/savings" element={<ProtectedRoute user={user}><SavingsPage /></ProtectedRoute>} />
          <Route path="/standing-orders" element={<ProtectedRoute user={user}><StandingOrdersPage /></ProtectedRoute>} />
          <Route path="/notifications" element={<ProtectedRoute user={user}><NotificationsPage /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute user={user}><ProfilePage /></ProtectedRoute>} />
          <Route path="/admin" element={<AdminRoute user={user}><AdminPage /></AdminRoute>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
