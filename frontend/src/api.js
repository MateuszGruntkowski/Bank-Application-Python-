const API_BASE = "/api";

class ApiClient {
  constructor() {
    this.token = localStorage.getItem("token");
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem("token", token);
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }

  getUser() {
    const raw = localStorage.getItem("user");
    return raw ? JSON.parse(raw) : null;
  }

  setUser(user) {
    localStorage.setItem("user", JSON.stringify(user));
  }

  async request(path, options = {}) {
    const headers = { "Content-Type": "application/json", ...options.headers };
    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }
    const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
    if (res.status === 401) {
      this.clearToken();
      window.location.href = "/login";
      return;
    }
    if (res.status === 501) {
      const data = await res.json();
      throw new Error(data.detail || "Feature not implemented yet");
    }
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || `Request failed: ${res.status}`);
    }
    if (res.headers.get("content-type")?.includes("application/json")) {
      return res.json();
    }
    return res;
  }

  get(path) { return this.request(path); }
  post(path, body) { return this.request(path, { method: "POST", body: JSON.stringify(body) }); }
  put(path, body) { return this.request(path, { method: "PUT", body: JSON.stringify(body) }); }
  delete(path) { return this.request(path, { method: "DELETE" }); }
}

const api = new ApiClient();
export default api;
