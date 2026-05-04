import { useState, useEffect } from "react";
import api from "../api";
import config from "../config";
import StatusMessage, { useApiCall } from "../components/StatusMessage";

export default function LoansPage() {
  const { loading, error, success, setError, setSuccess, execute } = useApiCall();
  const [loans, setLoans] = useState([]);
  const [amount, setAmount] = useState("");
  const [repayAmount, setRepayAmount] = useState("");
  const [selectedLoan, setSelectedLoan] = useState(null);
  const [schedule, setSchedule] = useState(null);
  const [tab, setTab] = useState("my-loans");

  const loadLoans = () => execute(async () => { const r = await api.get("/loans/me"); setLoans(Array.isArray(r) ? r : []); });

  useEffect(() => { loadLoans(); }, []);

  const handleApply = async (e) => {
    e.preventDefault();
    await execute(() => api.post("/loans/apply", { amount: parseFloat(amount) }));
    setAmount("");
    loadLoans();
  };

  const handleRepay = async (loanId) => {
    await execute(() => api.post(`/loans/${loanId}/repay`, { amount: parseFloat(repayAmount) }));
    setRepayAmount("");
    loadLoans();
  };

  const showSchedule = async (loanId) => {
    const result = await execute(() => api.get(`/loans/${loanId}/schedule`));
    if (result) { setSchedule(result); setSelectedLoan(loanId); }
  };

  const statusBadge = (status) => {
    const styles = { PENDING: "bg-yellow-100 text-yellow-700", APPROVED: "bg-primary-100 text-primary-700", REJECTED: "bg-red-100 text-red-700", PAID: "bg-gray-100 text-gray-600" };
    return <span className={`px-2 py-1 text-xs rounded-full font-medium ${styles[status] || "bg-gray-100"}`}>{status}</span>;
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Loans</h1>
        <p className="text-gray-500 mt-1">Apply for loans and manage repayments</p>
      </div>

      <div className="flex gap-2 mb-6">
        <button onClick={() => setTab("my-loans")} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === "my-loans" ? "bg-primary-600 text-white" : "bg-white text-gray-600 border border-gray-200"}`}>My Loans</button>
        <button onClick={() => setTab("apply")} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === "apply" ? "bg-primary-600 text-white" : "bg-white text-gray-600 border border-gray-200"}`}>Apply for Loan</button>
      </div>

      {error && <StatusMessage type="notImplemented" message={error} onDismiss={() => setError(null)} />}
      {success && <StatusMessage type="success" message={success} onDismiss={() => setSuccess(null)} />}

      {tab === "apply" && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 max-w-lg">
          <h2 className="text-lg font-semibold mb-4">Loan Application</h2>
          <form onSubmit={handleApply} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Amount (500 - 50,000 {config.currency})</label>
              <input id="loan-amount" type="number" min="500" max="50000" step="100" value={amount} onChange={(e) => setAmount(e.target.value)}
                className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" required />
            </div>
            <button type="submit" disabled={loading} className="px-6 py-2.5 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 transition-colors">Submit Application</button>
          </form>
        </div>
      )}

      {tab === "my-loans" && (
        <div className="space-y-4">
          {loans.length > 0 ? loans.map((loan) => (
            <div key={loan.id} className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold">Loan #{loan.id}</h3>
                {statusBadge(loan.status)}
              </div>
              <div className="grid grid-cols-2 gap-4 text-sm mb-4">
                <div><span className="text-gray-500">Amount:</span> <span className="font-medium">{loan.amount} {config.currency}</span></div>
                <div><span className="text-gray-500">Remaining:</span> <span className="font-medium">{loan.remaining ?? "—"} {config.currency}</span></div>
                <div><span className="text-gray-500">Date:</span> <span className="font-medium">{loan.created_at}</span></div>
                <div><span className="text-gray-500">Rate:</span> <span className="font-medium">{loan.interest_rate ?? "5"}%</span></div>
              </div>
              {loan.status === "APPROVED" && (
                <div className="flex gap-3 items-end">
                  <div className="flex-1">
                    <label className="block text-sm text-gray-600 mb-1">Repay amount</label>
                    <input type="number" step="0.01" min="0.01" value={repayAmount} onChange={(e) => setRepayAmount(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none" />
                  </div>
                  <button onClick={() => handleRepay(loan.id)} disabled={loading} className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700">Repay</button>
                  <button onClick={() => showSchedule(loan.id)} className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">Schedule</button>
                </div>
              )}
              {schedule && selectedLoan === loan.id && Array.isArray(schedule) && (
                <div className="mt-4 border-t pt-4">
                  <h4 className="font-medium text-sm mb-2">Repayment Schedule</h4>
                  <table className="w-full text-xs">
                    <thead><tr className="border-b"><th className="py-1 text-left">#</th><th className="py-1 text-left">Date</th><th className="py-1 text-right">Payment</th><th className="py-1 text-right">Principal</th><th className="py-1 text-right">Interest</th><th className="py-1 text-right">Remaining</th></tr></thead>
                    <tbody>{schedule.map((s, i) => (
                      <tr key={i} className="border-b border-gray-50"><td className="py-1">{s.number}</td><td className="py-1">{s.date}</td><td className="py-1 text-right">{s.payment}</td><td className="py-1 text-right">{s.principal}</td><td className="py-1 text-right">{s.interest}</td><td className="py-1 text-right">{s.remaining}</td></tr>
                    ))}</tbody>
                  </table>
                </div>
              )}
            </div>
          )) : (
            <div className="bg-white rounded-xl border border-gray-200 p-8 text-center text-gray-400">No loans found. Apply for your first loan!</div>
          )}
        </div>
      )}
    </div>
  );
}
