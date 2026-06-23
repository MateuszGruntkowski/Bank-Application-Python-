import {useState, useEffect} from "react";
import api from "../api";
import config from "../config";
import StatusMessage, {useApiCall} from "../components/StatusMessage";

export default function HistoryPage() {
    const {loading, error, success, setError, setSuccess, execute} = useApiCall();
    const [data, setData] = useState({transactions: [], total: 0, pages: 1});
    const [page, setPage] = useState(1);
    const [sortOrder, setSortOrder] = useState("desc");

    const loadHistory = () => {
        execute(async () => {
            const result = await api.get(`/accounts/me/transactions?page=${page}&per_page=10&sort_order=${sortOrder}`);
            if (result) setData(result);
        });
    };

    useEffect(() => {
        loadHistory();
    }, [page, sortOrder]);

    const downloadCsv = async () => {
        try {
            setError(null);
            setSuccess(null);
            // Expected to return a CSV string or a Blob
            const result = await api.get("/accounts/me/statement", {responseType: 'blob'});
            if (result) {
                // Simple fallback if the API returns 501 JSON
                if (result.detail && result.detail.includes("Not implemented")) {
                    setError(result.detail);
                    return;
                }
                let fileData;
                if (typeof result.blob === 'function') {
                    fileData = await result.blob();
                } else if (result.data) {
                    fileData = result.data;
                } else {
                    fileData = result;
                }
                const blob = new Blob([fileData], {type: 'text/csv'});
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `statement_${new Date().toISOString().split('T')[0]}.csv`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                setSuccess("Statement downloaded successfully");
            }
        } catch (e) {
            if (e.message && e.message.includes("501")) {
                setError("Not implemented - waiting for StatementGenerator");
            } else {
                setError("Failed to download statement");
            }
        }
    };

    return (
        <div>
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Transaction History</h1>
                    <p className="text-gray-500 mt-1">View your past account activity</p>
                </div>
                <button
                    onClick={downloadCsv}
                    disabled={loading}
                    className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors"
                >
                    📥 Download Statement (CSV)
                </button>
            </div>

            {error && <StatusMessage type="notImplemented" message={error} onDismiss={() => setError(null)}/>}
            {success && <StatusMessage type="success" message={success} onDismiss={() => setSuccess(null)}/>}

            <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
                <div className="flex justify-end p-4 border-b border-gray-100 bg-gray-50">
                    <select
                        value={sortOrder}
                        onChange={(e) => setSortOrder(e.target.value)}
                        className="text-sm border-gray-200 rounded-lg outline-none"
                    >
                        <option value="desc">Newest first</option>
                        <option value="asc">Oldest first</option>
                    </select>
                </div>

                {data?.transactions?.length > 0 ? (
                    <div>
                        <table className="w-full text-sm">
                            <thead>
                            <tr className="border-b border-gray-100 bg-gray-50">
                                <th className="text-left py-3 px-4 text-gray-500 font-medium">Date</th>
                                <th className="text-left py-3 px-4 text-gray-500 font-medium">Type</th>
                                <th className="text-left py-3 px-4 text-gray-500 font-medium">Title</th>
                                <th className="text-right py-3 px-4 text-gray-500 font-medium">Amount</th>
                            </tr>
                            </thead>
                            <tbody>
                            {data.transactions.map((tx, i) => {
                                const isIncoming = tx.type === "IN";
                                return (
                                    <tr key={i} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                                        <td className="py-3 px-4 text-gray-600">{tx.date || tx.created_at}</td>
                                        <td className="py-3 px-4">
                        <span
                            className={`inline-block px-2 py-1 text-xs rounded-md ${isIncoming ? 'bg-primary-50 text-primary-700' : 'bg-gray-100 text-gray-700'}`}>
                          {tx.type}
                        </span>
                                        </td>
                                        <td className="py-3 px-4">{tx.title}</td>
                                        <td className={`py-3 px-4 text-right font-medium ${isIncoming ? "text-primary-600" : "text-red-500"}`}>
                                            {isIncoming ? "+" : "-"}{tx.amount} {config.currency}
                                        </td>
                                    </tr>
                                );
                            })}
                            </tbody>
                        </table>

                        {/* Pagination Controls */}
                        <div className="flex items-center justify-between p-4 border-t border-gray-100 bg-white">
              <span className="text-sm text-gray-500">
                Page {page} of {Math.max(1, data.pages)} (Total: {data.total})
              </span>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => setPage(p => Math.max(1, p - 1))}
                                    disabled={page <= 1 || loading}
                                    className="px-3 py-1.5 text-sm border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                                >
                                    Previous
                                </button>
                                <button
                                    onClick={() => setPage(p => Math.min(data.pages, p + 1))}
                                    disabled={page >= data.pages || loading}
                                    className="px-3 py-1.5 text-sm border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                                >
                                    Next
                                </button>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="p-8 text-center text-gray-400">
                        <span className="text-4xl block mb-2">📊</span>
                        <p>No transactions found for this period.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
