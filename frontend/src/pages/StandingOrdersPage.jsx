import { useState, useEffect } from "react";
import api from "../api";
import config from "../config";
import StatusMessage, { useApiCall } from "../components/StatusMessage";

export default function StandingOrdersPage() {
  const { loading, error, success, setError, setSuccess, execute } = useApiCall();
  const [orders, setOrders] = useState([]);
  const [form, setForm] = useState({ to_account_number: "", amount: "", title: "", frequency: "MONTHLY" });

  const loadOrders = () => execute(async () => { const r = await api.get("/standing-orders"); setOrders(Array.isArray(r) ? r : []); });
  useEffect(() => { loadOrders(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    await execute(() => api.post("/standing-orders", { ...form, amount: parseFloat(form.amount) }));
    setForm({ to_account_number: "", amount: "", title: "", frequency: "MONTHLY" });
    loadOrders();
  };

  const handleCancel = async (id) => {
    await execute(() => api.delete(`/standing-orders/${id}`));
    loadOrders();
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Standing Orders</h1>
        <p className="text-gray-500 mt-1">Manage recurring payments</p>
      </div>

      {error && <StatusMessage type="notImplemented" message={error} onDismiss={() => setError(null)} />}
      {success && <StatusMessage type="success" message={success} onDismiss={() => setSuccess(null)} />}

      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6 max-w-lg">
        <h2 className="text-lg font-semibold mb-4">Create Standing Order</h2>
        <form onSubmit={handleCreate} className="space-y-3">
          <input placeholder="Recipient account number" value={form.to_account_number} onChange={(e) => setForm({ ...form, to_account_number: e.target.value })}
            className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" required />
          <input type="number" step="0.01" min="0.01" placeholder={`Amount (${config.currency})`} value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })}
            className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" required />
          <input placeholder="Title / description" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })}
            className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" required />
          <select value={form.frequency} onChange={(e) => setForm({ ...form, frequency: e.target.value })}
            className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none">
            <option value="WEEKLY">Weekly</option>
            <option value="MONTHLY">Monthly</option>
          </select>
          <button type="submit" disabled={loading} className="px-6 py-2.5 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 transition-colors">Create Order</button>
        </form>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-lg font-semibold mb-4">Active Orders</h2>
        {orders.length > 0 ? (
          <div className="space-y-3">
            {orders.map((o) => (
              <div key={o.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium">{o.title}</p>
                  <p className="text-sm text-gray-500">{o.to_account_number} · {o.frequency} · {o.amount} {config.currency}</p>
                  <p className="text-xs text-gray-400">Next: {o.next_execution_date}</p>
                </div>
                <button onClick={() => handleCancel(o.id)} className="px-3 py-1.5 text-sm bg-red-50 text-red-600 rounded-lg hover:bg-red-100">Cancel</button>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-400 text-center py-6">No standing orders yet.</p>
        )}
      </div>
    </div>
  );
}
