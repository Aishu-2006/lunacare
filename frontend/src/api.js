const API_BASE = "http://127.0.0.1:5000";

export async function checkBackend() {
  const response = await fetch(`${API_BASE}/api/health`);
  return response.json();
}
