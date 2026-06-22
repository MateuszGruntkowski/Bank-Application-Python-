import { useState, useEffect } from "react";
import api from "../api";
import config from "../config";
import StatusMessage, { useApiCall } from "../components/StatusMessage";

function StatCard({ label, value, icon, color = "primary" }) {
  const colors = {
    primary: "bg-primary-50 text-primary-700 border-primary-100",
    blue: "bg-blue-50 text-blue-700 border-blue-100",
    amber: "bg-amber-50 text-amber-700 border-amber-100",
    purple: "bg-purple-50 text-purple-700 border-purple-100",
  };
  return (
    <div className={`rounded-xl border p-5 ${colors[color]}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-2xl">{icon}</span>
      </div>
      <p className="text-2xl font-bold">{value}</p>
      <p className="text-sm opacity-75 mt-1">{label}</p>
    </div>
  );
}

export default function DashboardPage() {
  const { loading, error, execute } = useApiCall();
  const [data, setData] = useState(null);

  useEffect(() => {
    execute(async () => {
      const result = await api.get("/dashboard");
      setData(result);
      return result;
    });
  }, []);

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">Welcome to {config.bankName}</p>
      </div>

      {error && <StatusMessage type="notImplemented" message={error} />}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Balance" value={data?.balance ?? "—"} icon="💰" color="primary" />
        <StatCard label="Transactions" value={data?.transaction_count ?? "—"} icon="📈" color="blue" />
        <StatCard label="Notifications" value={data?.unread_notifications ?? "—"} icon="🔔" color="amber" />
        <StatCard label="Active Loans" value={data?.active_loans ?? "—"} icon="🏦" color="purple" />
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Transactions</h2>
        {data?.recent_transactions?.length > 0 ? (
          <table className="w-full text-sm">
            <thead><tr className="border-b border-gray-100">
              <th className="text-left py-2 text-gray-500 font-medium">Date</th>
              <th className="text-left py-2 text-gray-500 font-medium">Title</th>
              <th className="text-right py-2 text-gray-500 font-medium">Amount</th>
            </tr></thead>
            <tbody>
              {data.recent_transactions.map((tx, i) => {
                const isIncoming = tx.type === "IN";
                return (
                  <tr key={i} className="border-b border-gray-50">
                    <td className="py-3 text-gray-600">{tx.created_at}</td>
                    <td className="py-3">{tx.title}</td>
                    <td className={`py-3 text-right font-medium ${isIncoming ? "text-primary-600" : "text-red-500"}`}>
                      {isIncoming ? "+" : "-"}{tx.amount} {config.currency}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : (
          <p className="text-gray-400 text-center py-8">No transactions yet.</p>
        )}
      </div>
    </div>
  );
}
