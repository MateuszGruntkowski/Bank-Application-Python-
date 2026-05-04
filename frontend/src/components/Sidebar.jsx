import { NavLink, useLocation } from "react-router-dom";
import config from "../config";

const navItems = [
  { path: "/", label: "Dashboard", icon: "📊" },
  { path: "/history", label: "History", icon: "🕒" },
  { path: "/transfers", label: "Transfers", icon: "💸" },
  { path: "/atm", label: "ATM", icon: "🏧" },
  { path: "/loans", label: "Loans", icon: "🏦" },
  { path: "/savings", label: "Savings Goals", icon: "🎯" },
  { path: "/standing-orders", label: "Standing Orders", icon: "🔄" },
  { path: "/notifications", label: "Notifications", icon: "🔔" },
  { path: "/profile", label: "Profile", icon: "👤" },
];

const adminItems = [
  { path: "/admin", label: "Admin Panel", icon: "⚙️" },
];

export default function Sidebar({ user, onLogout }) {
  const location = useLocation();
  const items = user?.is_admin ? [...navItems, ...adminItems] : navItems;

  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col h-screen shrink-0">
      <div className="p-6 border-b border-gray-100">
        <h1 className="text-xl font-bold text-primary-600">{config.bankName}</h1>
        <p className="text-xs text-gray-400 mt-1">{config.bankTagline}</p>
      </div>

      <nav className="flex-1 overflow-y-auto p-4 space-y-1">
        {items.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                isActive
                  ? "bg-primary-50 text-primary-700 shadow-sm"
                  : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
              }`
            }
          >
            <span className="text-lg">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-gray-100">
        <div className="flex items-center gap-3 px-3 py-2 mb-2">
          <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-bold text-sm">
            {user?.username?.[0]?.toUpperCase() || "?"}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">{user?.username}</p>
            <p className="text-xs text-gray-400">{user?.is_admin ? "Admin" : "User"}</p>
          </div>
        </div>
        <button
          onClick={onLogout}
          className="w-full px-4 py-2 text-sm text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
        >
          Logout
        </button>
      </div>
    </aside>
  );
}
