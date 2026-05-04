import { useState, useEffect } from "react";
import api from "../api";
import config from "../config";
import StatusMessage, { useApiCall } from "../components/StatusMessage";

export default function ProfilePage() {
  const { loading, error, success, setError, setSuccess, execute } = useApiCall();
  const [profile, setProfile] = useState({ first_name: "", last_name: "", phone: "" });
  const [limits, setLimits] = useState({ max_single_transfer: "", max_daily_amount: "", max_daily_count: "" });
  const [tab, setTab] = useState("profile");

  useEffect(() => {
    execute(async () => { const r = await api.get("/profile"); setProfile(r); });
    execute(async () => { const r = await api.get("/limits"); setLimits(r); });
  }, []);

  const handleProfileSave = async (e) => {
    e.preventDefault();
    await execute(() => api.put("/profile", profile));
  };

  const handleLimitsSave = async (e) => {
    e.preventDefault();
    await execute(() => api.put("/limits", {
      max_single_transfer: parseFloat(limits.max_single_transfer) || null,
      max_daily_amount: parseFloat(limits.max_daily_amount) || null,
      max_daily_count: parseInt(limits.max_daily_count) || null,
    }));
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Profile & Settings</h1>
        <p className="text-gray-500 mt-1">Manage your personal information and limits</p>
      </div>

      <div className="flex gap-2 mb-6">
        <button onClick={() => setTab("profile")} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === "profile" ? "bg-primary-600 text-white" : "bg-white text-gray-600 border border-gray-200"}`}>Profile</button>
        <button onClick={() => setTab("limits")} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === "limits" ? "bg-primary-600 text-white" : "bg-white text-gray-600 border border-gray-200"}`}>Transaction Limits</button>
      </div>

      {error && <StatusMessage type="notImplemented" message={error} onDismiss={() => setError(null)} />}
      {success && <StatusMessage type="success" message={success} onDismiss={() => setSuccess(null)} />}

      {tab === "profile" && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 max-w-lg">
          <h2 className="text-lg font-semibold mb-4">Personal Information</h2>
          <form onSubmit={handleProfileSave} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
              <input value={profile.first_name || ""} onChange={(e) => setProfile({ ...profile, first_name: e.target.value })}
                className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
              <input value={profile.last_name || ""} onChange={(e) => setProfile({ ...profile, last_name: e.target.value })}
                className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
              <input value={profile.phone || ""} onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <button type="submit" disabled={loading} className="px-6 py-2.5 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 transition-colors">Save Profile</button>
          </form>
        </div>
      )}

      {tab === "limits" && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 max-w-lg">
          <h2 className="text-lg font-semibold mb-4">Transaction Limits</h2>
          <form onSubmit={handleLimitsSave} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Max Single Transfer ({config.currency})</label>
              <input type="number" step="100" value={limits.max_single_transfer || ""} onChange={(e) => setLimits({ ...limits, max_single_transfer: e.target.value })}
                className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Max Daily Amount ({config.currency})</label>
              <input type="number" step="100" value={limits.max_daily_amount || ""} onChange={(e) => setLimits({ ...limits, max_daily_amount: e.target.value })}
                className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Max Daily Transaction Count</label>
              <input type="number" min="1" value={limits.max_daily_count || ""} onChange={(e) => setLimits({ ...limits, max_daily_count: e.target.value })}
                className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <button type="submit" disabled={loading} className="px-6 py-2.5 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 transition-colors">Save Limits</button>
          </form>
        </div>
      )}
    </div>
  );
}
