import { useState, useEffect } from "react";
import api from "../api";
import config from "../config";
import StatusMessage, { useApiCall } from "../components/StatusMessage";

export default function TransfersPage() {
  const { loading, error, success, setError, setSuccess, execute } = useApiCall();
  const [form, setForm] = useState({ to_account_number: "", amount: "", title: "" });
  const [recipients, setRecipients] = useState([]);
  const [newRecipient, setNewRecipient] = useState({ name: "", account_number: "" });
  const [tab, setTab] = useState("transfer"); // transfer | recipients

  useEffect(() => {
    execute(async () => { const r = await api.get("/recipients"); setRecipients(r); });
  }, []);

  const handleTransfer = async (e) => {
    e.preventDefault();
    const result = await execute(() => api.post("/transfers", { ...form, amount: parseFloat(form.amount) }));
    if (result) setForm({ to_account_number: "", amount: "", title: "" });
  };

  const handleExternalTransfer = async (e) => {
    e.preventDefault();
    const result = await execute(() => api.post("/transfers/external", { ...form, amount: parseFloat(form.amount) }));
    if (result) setForm({ to_account_number: "", amount: "", title: "" });
  };

  const handleAddRecipient = async (e) => {
    e.preventDefault();
    const result = await execute(() => api.post("/recipients", newRecipient));
    if (result) { setNewRecipient({ name: "", account_number: "" }); execute(async () => { const r = await api.get("/recipients"); setRecipients(r); }); }
  };

  const handleDeleteRecipient = async (id) => {
    await execute(() => api.delete(`/recipients/${id}`));
    execute(async () => { const r = await api.get("/recipients"); setRecipients(r); });
  };

  const selectRecipient = (r) => {
    setForm({ ...form, to_account_number: r.account_number });
    setTab("transfer");
  };

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Transfers</h1>
        <p className="text-gray-500 mt-1">Send money and manage recipients</p>
      </div>

      <div className="flex gap-2 mb-6">
        <button onClick={() => setTab("transfer")} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === "transfer" ? "bg-primary-600 text-white" : "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50"}`}>Make Transfer</button>
        <button onClick={() => setTab("recipients")} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === "recipients" ? "bg-primary-600 text-white" : "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50"}`}>Saved Recipients</button>
      </div>

      {error && <StatusMessage type="notImplemented" message={error} onDismiss={() => setError(null)} />}
      {success && <StatusMessage type="success" message={success} onDismiss={() => setSuccess(null)} />}

      {tab === "transfer" && (
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-lg font-semibold mb-4">New Transfer</h2>
          <form onSubmit={handleTransfer} className="space-y-4 max-w-lg">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Recipient Account Number</label>
              <input id="transfer-account" value={form.to_account_number} onChange={update("to_account_number")} placeholder="PL00000000000000000000000000"
                className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Amount ({config.currency})</label>
              <input id="transfer-amount" type="number" step="0.01" min="0.01" value={form.amount} onChange={update("amount")}
                className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
              <input id="transfer-title" value={form.title} onChange={update("title")}
                className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none" required />
            </div>
            <div className="flex gap-3">
              <button type="submit" disabled={loading} className="px-6 py-2.5 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 transition-colors">Send Transfer</button>
              <button type="button" onClick={handleExternalTransfer} disabled={loading} className="px-6 py-2.5 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 disabled:opacity-50 transition-colors">External Transfer</button>
            </div>
          </form>
        </div>
      )}

      {tab === "recipients" && (
        <div className="space-y-6">
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-lg font-semibold mb-4">Add Recipient</h2>
            <form onSubmit={handleAddRecipient} className="flex gap-3 flex-wrap">
              <input placeholder="Name" value={newRecipient.name} onChange={(e) => setNewRecipient({ ...newRecipient, name: e.target.value })}
                className="flex-1 min-w-[200px] px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" required />
              <input placeholder="Account number" value={newRecipient.account_number} onChange={(e) => setNewRecipient({ ...newRecipient, account_number: e.target.value })}
                className="flex-1 min-w-[200px] px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" required />
              <button type="submit" disabled={loading} className="px-6 py-2.5 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 transition-colors">Add</button>
            </form>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-lg font-semibold mb-4">Saved Recipients</h2>
            {Array.isArray(recipients) && recipients.length > 0 ? (
              <div className="space-y-2">
                {recipients.map((r) => (
                  <div key={r.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium">{r.name}</p>
                      <p className="text-sm text-gray-500">{r.account_number}</p>
                    </div>
                    <div className="flex gap-2">
                      <button onClick={() => selectRecipient(r)} className="px-3 py-1.5 text-sm bg-primary-50 text-primary-700 rounded-lg hover:bg-primary-100">Use</button>
                      <button onClick={() => handleDeleteRecipient(r.id)} className="px-3 py-1.5 text-sm bg-red-50 text-red-600 rounded-lg hover:bg-red-100">Remove</button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-400 text-center py-6">No saved recipients yet.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
