import { useState, useEffect } from "react";
import api from "../api";
import config from "../config";
import StatusMessage, { useApiCall } from "../components/StatusMessage";

export default function SavingsPage() {
  const { loading, error, success, setError, setSuccess, execute } = useApiCall();
  const [goals, setGoals] = useState([]);
  const [form, setForm] = useState({ name: "", target_amount: "", deadline: "" });
  const [fundAmounts, setFundAmounts] = useState({});

  const loadGoals = () => execute(async () => { const r = await api.get("/savings-goals"); setGoals(Array.isArray(r) ? r : []); });
  useEffect(() => { loadGoals(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    await execute(() => api.post("/savings-goals", { ...form, target_amount: parseFloat(form.target_amount) }));
    setForm({ name: "", target_amount: "", deadline: "" });
    loadGoals();
  };

  const handleDeposit = async (id) => {
    await execute(() => api.post(`/savings-goals/${id}/deposit`, { amount: parseFloat(fundAmounts[id] || 0) }));
    setFundAmounts({ ...fundAmounts, [id]: "" });
    loadGoals();
  };

  const handleWithdraw = async (id) => {
    await execute(() => api.post(`/savings-goals/${id}/withdraw`, { amount: parseFloat(fundAmounts[id] || 0) }));
    setFundAmounts({ ...fundAmounts, [id]: "" });
    loadGoals();
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Savings Goals</h1>
        <p className="text-gray-500 mt-1">Set goals and track your progress</p>
      </div>

      {error && <StatusMessage type="notImplemented" message={error} onDismiss={() => setError(null)} />}
      {success && <StatusMessage type="success" message={success} onDismiss={() => setSuccess(null)} />}

      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6 max-w-lg">
        <h2 className="text-lg font-semibold mb-4">Create New Goal</h2>
        <form onSubmit={handleCreate} className="space-y-3">
          <input placeholder="Goal name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" required />
          <input type="number" placeholder={`Target amount (${config.currency})`} min="1" step="0.01" value={form.target_amount} onChange={(e) => setForm({ ...form, target_amount: e.target.value })}
            className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" required />
          <input type="date" value={form.deadline} onChange={(e) => setForm({ ...form, deadline: e.target.value })}
            className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" required />
          <button type="submit" disabled={loading} className="px-6 py-2.5 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 transition-colors">Create Goal</button>
        </form>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {goals.map((goal) => {
          const pct = goal.target_amount > 0 ? Math.min(100, (goal.current_amount / goal.target_amount) * 100) : 0;
          return (
            <div key={goal.id} className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-semibold">{goal.name}</h3>
                {goal.is_completed && <span className="px-2 py-1 text-xs bg-primary-100 text-primary-700 rounded-full font-medium">Completed ✓</span>}
              </div>
              <div className="mb-3">
                <div className="flex justify-between text-sm mb-1">
                  <span>{goal.current_amount} {config.currency}</span>
                  <span className="text-gray-500">{goal.target_amount} {config.currency}</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-3">
                  <div className="bg-primary-500 h-3 rounded-full transition-all duration-500" style={{ width: `${pct}%` }}></div>
                </div>
                <p className="text-xs text-gray-400 mt-1">Deadline: {goal.deadline}</p>
              </div>
              {!goal.is_completed && (
                <div className="flex gap-2 items-end">
                  <input type="number" step="0.01" min="0.01" placeholder="Amount" value={fundAmounts[goal.id] || ""} onChange={(e) => setFundAmounts({ ...fundAmounts, [goal.id]: e.target.value })}
                    className="flex-1 px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none" />
                  <button onClick={() => handleDeposit(goal.id)} className="px-3 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700">Add</button>
                  <button onClick={() => handleWithdraw(goal.id)} className="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">Take</button>
                </div>
              )}
            </div>
          );
        })}
        {goals.length === 0 && <div className="col-span-2 bg-white rounded-xl border border-gray-200 p-8 text-center text-gray-400">No savings goals yet.</div>}
      </div>
    </div>
  );
}
