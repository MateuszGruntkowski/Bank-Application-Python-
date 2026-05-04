import { useState, useEffect } from "react";
import api from "../api";
import StatusMessage, { useApiCall } from "../components/StatusMessage";

export default function NotificationsPage() {
  const { loading, error, execute } = useApiCall();
  const [notifications, setNotifications] = useState([]);

  const load = () => execute(async () => { const r = await api.get("/notifications"); setNotifications(Array.isArray(r) ? r : []); });
  useEffect(() => { load(); }, []);

  const markRead = async (id) => {
    await execute(() => api.put(`/notifications/${id}/read`));
    load();
  };

  const typeIcon = { INFO: "ℹ️", WARNING: "⚠️", SUCCESS: "✅" };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Notifications</h1>
        <p className="text-gray-500 mt-1">Stay updated with your account activity</p>
      </div>

      {error && <StatusMessage type="notImplemented" message={error} />}

      <div className="space-y-2">
        {notifications.length > 0 ? notifications.map((n) => (
          <div key={n.id} className={`bg-white rounded-xl border p-4 flex items-start gap-3 transition-colors ${n.is_read ? "border-gray-100 opacity-60" : "border-primary-200 bg-primary-50/30"}`}>
            <span className="text-xl mt-0.5">{typeIcon[n.type] || "📌"}</span>
            <div className="flex-1">
              <p className="font-medium text-sm">{n.title}</p>
              <p className="text-sm text-gray-600">{n.message}</p>
              <p className="text-xs text-gray-400 mt-1">{n.created_at}</p>
            </div>
            {!n.is_read && (
              <button onClick={() => markRead(n.id)} className="px-3 py-1 text-xs bg-primary-100 text-primary-700 rounded-lg hover:bg-primary-200">Mark read</button>
            )}
          </div>
        )) : (
          <div className="bg-white rounded-xl border border-gray-200 p-8 text-center text-gray-400">No notifications yet.</div>
        )}
      </div>
    </div>
  );
}
