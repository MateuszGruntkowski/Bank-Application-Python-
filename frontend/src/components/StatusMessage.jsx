import { useState } from "react";

export default function StatusMessage({ type = "error", message, onDismiss }) {
  if (!message) return null;

  const styles = {
    error: "bg-red-50 border-red-200 text-red-700",
    success: "bg-primary-50 border-primary-200 text-primary-700",
    warning: "bg-yellow-50 border-yellow-200 text-yellow-700",
    info: "bg-blue-50 border-blue-200 text-blue-700",
    notImplemented: "bg-amber-50 border-amber-300 text-amber-800",
  };

  return (
    <div className={`border rounded-lg p-4 mb-4 flex items-center justify-between ${styles[type] || styles.error}`}>
      <p className="text-sm">{message}</p>
      {onDismiss && (
        <button onClick={onDismiss} className="ml-4 text-lg leading-none opacity-50 hover:opacity-100">&times;</button>
      )}
    </div>
  );
}

export function useApiCall() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const execute = async (apiCall) => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const result = await apiCall();
      setSuccess("Operation completed successfully");
      return result;
    } catch (err) {
      const msg = err.message || "An error occurred";
      if (msg.includes("Not implemented")) {
        setError(`🚧 ${msg}`);
      } else {
        setError(msg);
      }
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { loading, error, success, setError, setSuccess, execute };
}
