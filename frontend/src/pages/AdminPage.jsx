import { useState, useEffect } from "react";
import api from "../api";
import config from "../config";
import StatusMessage, { useApiCall } from "../components/StatusMessage";

export default function AdminPage() {
  const { loading, error, success, setError, setSuccess, execute } = useApiCall();
  const [tab, setTab] = useState("stats");
  const [stats, setStats] = useState(null);
  const [loans, setLoans] = useState([]);
  const [loanFilter, setLoanFilter] = useState("");
  const [feeAmount, setFeeAmount] = useState("5");
  const [rejectReason, setRejectReason] = useState("");
  const [reversalReason, setReversalReason] = useState("");
  const [reversalTxId, setReversalTxId] = useState("");

  const loadStats = () => execute(async () => { const r = await api.get("/admin/stats"); setStats(r); });
  const loadLoans = () => execute(async () => { const r = await api.get(`/admin/loans?status=${loanFilter}`); setLoans(Array.isArray(r) ? r : []); });

  useEffect(() => { if (tab === "stats") loadStats(); if (tab === "loans") loadLoans(); }, [tab, loanFilter]);

  const [scores, setScores] = useState({});

  const checkScore = async (userId) => {
    if (scores[userId]) return;
    const result = await execute(() => api.get(`/admin/scoring/${userId}`));
    if (result) setScores(prev => ({ ...prev, [userId]: result }));
  };

  const approveLoan = async (id) => { await execute(() => api.post(`/admin/loans/${id}/approve`)); loadLoans(); };
  const rejectLoan = async (id) => { await execute(() => api.post(`/admin/loans/${id}/reject`, { reason: rejectReason || "Rejected by admin" })); setRejectReason(""); loadLoans(); };
  const chargeFees = async () => { await execute(() => api.post("/admin/charge-fees", { amount: parseFloat(feeAmount) })); };
  const executeOrders = async () => { await execute(() => api.post("/admin/execute-standing-orders")); };
  const reverseTransaction = async () => { await execute(() => api.post(`/admin/transactions/${reversalTxId}/reverse`, { reason: reversalReason })); setReversalTxId(""); setReversalReason(""); };
  const exportData = async () => { await execute(() => api.get("/admin/export")); };

  const tabs = [
    { id: "stats", label: "Statistics" }, { id: "loans", label: "Loan Management" },
    { id: "operations", label: "Operations" }, { id: "reversal", label: "Transaction Reversal" },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Admin Panel</h1>
        <p className="text-gray-500 mt-1">Bank management and administration</p>
      </div>

      <div className="flex gap-2 mb-6 flex-wrap">
        {tabs.map((t) => (
          <button key={t.id} onClick={() => setTab(t.id)} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === t.id ? "bg-primary-600 text-white" : "bg-white text-gray-600 border border-gray-200"}`}>{t.label}</button>
        ))}
      </div>

      {error && <StatusMessage type="notImplemented" message={error} onDismiss={() => setError(null)} />}
      {success && <StatusMessage type="success" message={success} onDismiss={() => setSuccess(null)} />}

      {tab === "stats" && (
        <div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            {[
              { label: "Total Deposits", value: stats?.total_deposits, icon: "💰" },
              { label: "Active Clients", value: stats?.active_clients, icon: "👥" },
              { label: "Total Debt", value: stats?.total_debt, icon: "📊" },
              { label: "Average Balance", value: stats?.average_balance, icon: "📈" },
              { label: "Transactions (30d)", value: stats?.transactions_30d, icon: "🔄" },
              { label: "Active Loans", value: stats?.active_loans, icon: "🏦" },
            ].map((s, i) => (
              <div key={i} className="bg-white rounded-xl border border-gray-200 p-5">
                <span className="text-2xl">{s.icon}</span>
                <p className="text-2xl font-bold mt-2">{s.value ?? "—"}</p>
                <p className="text-sm text-gray-500">{s.label}</p>
              </div>
            ))}
          </div>
          <button onClick={exportData} className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm font-medium">📥 Export Report (JSON)</button>
        </div>
      )}

      {tab === "loans" && (
        <div>
          <div className="flex gap-2 mb-4">
            {["", "PENDING", "APPROVED", "REJECTED", "PAID"].map((f) => (
              <button key={f} onClick={() => setLoanFilter(f)} className={`px-3 py-1.5 rounded-lg text-xs font-medium ${loanFilter === f ? "bg-primary-600 text-white" : "bg-gray-100 text-gray-600"}`}>{f || "All"}</button>
            ))}
          </div>
          <div className="space-y-3">
            {loans.map((loan) => (
              <div key={loan.id} className="bg-white rounded-xl border border-gray-200 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Loan #{loan.id} — User: {loan.user_id}</p>
                    <p className="text-sm text-gray-500 mb-2">{loan.amount} {config.currency} · Status: {loan.status} · {loan.created_at}</p>
                    
                    {loan.status === "PENDING" && (
                      <div className="mt-2 text-sm bg-gray-50 p-2 rounded border border-gray-100 inline-block">
                        {scores[loan.user_id] ? (
                          <div>
                            <span className="font-medium text-gray-700">Scoring: {scores[loan.user_id].score} pts</span>
                            <span className={`ml-2 px-2 py-0.5 rounded text-xs ${
                              scores[loan.user_id].recommendation === 'APPROVE' ? 'bg-green-100 text-green-700' :
                              scores[loan.user_id].recommendation === 'REJECT' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'
                            }`}>
                              {scores[loan.user_id].recommendation}
                            </span>
                          </div>
                        ) : (
                          <button onClick={() => checkScore(loan.user_id)} className="text-primary-600 hover:text-primary-700 text-xs font-medium">
                            Calculate Credit Score
                          </button>
                        )}
                      </div>
                    )}
                  </div>
                  {loan.status === "PENDING" && (
                    <div className="flex flex-col items-end gap-2">
                      <div className="flex gap-2">
                        <button onClick={() => approveLoan(loan.id)} className="px-3 py-1.5 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700">Approve</button>
                        <button onClick={() => rejectLoan(loan.id)} className="px-3 py-1.5 text-sm bg-red-100 text-red-600 rounded-lg hover:bg-red-200">Reject</button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loans.length === 0 && <div className="bg-white rounded-xl border p-8 text-center text-gray-400">No loans found.</div>}
          </div>
        </div>
      )}

      {tab === "operations" && (
        <div className="space-y-4 max-w-lg">
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h3 className="font-semibold mb-3">Charge Account Fees</h3>
            <div className="flex gap-3 items-end">
              <div className="flex-1">
                <label className="block text-sm text-gray-600 mb-1">Fee amount ({config.currency})</label>
                <input type="number" step="0.01" value={feeAmount} onChange={(e) => setFeeAmount(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none" />
              </div>
              <button onClick={chargeFees} disabled={loading} className="px-4 py-2 bg-amber-500 text-white rounded-lg text-sm hover:bg-amber-600">Charge All</button>
            </div>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h3 className="font-semibold mb-3">Execute Standing Orders</h3>
            <p className="text-sm text-gray-500 mb-3">Run all pending standing orders now.</p>
            <button onClick={executeOrders} disabled={loading} className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700">Execute Now</button>
          </div>
        </div>
      )}

      {tab === "reversal" && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 max-w-lg">
          <h3 className="font-semibold mb-3">Reverse Transaction</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Transaction ID</label>
              <input type="number" value={reversalTxId} onChange={(e) => setReversalTxId(e.target.value)}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Reason</label>
              <input value={reversalReason} onChange={(e) => setReversalReason(e.target.value)}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <button onClick={reverseTransaction} disabled={loading || !reversalTxId} className="px-4 py-2 bg-red-500 text-white rounded-lg text-sm hover:bg-red-600 disabled:opacity-50">Reverse Transaction</button>
          </div>
        </div>
      )}
    </div>
  );
}
