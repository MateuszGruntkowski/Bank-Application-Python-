import { useState } from "react";
import api from "../api";
import config from "../config";
import StatusMessage, { useApiCall } from "../components/StatusMessage";

export default function ATMPage() {
  const { loading, error, success, setError, setSuccess, execute } = useApiCall();
  const [amount, setAmount] = useState("");
  const [mode, setMode] = useState("deposit");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const endpoint = mode === "deposit" ? "/atm/deposit" : "/atm/withdraw";
    const result = await execute(() => api.post(endpoint, { amount: parseFloat(amount) }));
    if (result) setAmount("");
  };

  const quickAmounts = [50, 100, 200, 500, 1000];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">ATM</h1>
        <p className="text-gray-500 mt-1">Deposit or withdraw cash</p>
      </div>

      {error && <StatusMessage type="notImplemented" message={error} onDismiss={() => setError(null)} />}
      {success && <StatusMessage type="success" message={success} onDismiss={() => setSuccess(null)} />}

      <div className="max-w-md">
        <div className="flex gap-2 mb-6">
          <button onClick={() => setMode("deposit")} className={`flex-1 py-3 rounded-lg text-sm font-medium transition-colors ${mode === "deposit" ? "bg-primary-600 text-white" : "bg-white text-gray-600 border border-gray-200"}`}>
            💵 Deposit
          </button>
          <button onClick={() => setMode("withdraw")} className={`flex-1 py-3 rounded-lg text-sm font-medium transition-colors ${mode === "withdraw" ? "bg-red-500 text-white" : "bg-white text-gray-600 border border-gray-200"}`}>
            💳 Withdraw
          </button>
        </div>

        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-lg font-semibold mb-4">{mode === "deposit" ? "Cash Deposit" : "Cash Withdrawal"}</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Amount ({config.currency})</label>
              <input id="atm-amount" type="number" step="0.01" min="0.01" value={amount} onChange={(e) => setAmount(e.target.value)}
                className="w-full px-4 py-3 text-xl border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none text-center font-bold" required />
            </div>
            <div className="flex gap-2 flex-wrap">
              {quickAmounts.map((qa) => (
                <button key={qa} type="button" onClick={() => setAmount(String(qa))}
                  className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium">
                  {qa} {config.currency}
                </button>
              ))}
            </div>
            <button type="submit" disabled={loading}
              className={`w-full py-3 rounded-lg font-medium text-white transition-colors disabled:opacity-50 ${mode === "deposit" ? "bg-primary-600 hover:bg-primary-700" : "bg-red-500 hover:bg-red-600"}`}>
              {loading ? "Processing..." : mode === "deposit" ? "Deposit" : "Withdraw"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
