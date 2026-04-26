const TOKEN_KEY = 'solace_token';
export const saveToken = (t: string) => localStorage.setItem(TOKEN_KEY, t);
export const clearToken = () => localStorage.removeItem(TOKEN_KEY);
export const getToken = () => localStorage.getItem(TOKEN_KEY);

export async function apiFetch(path: string, init: RequestInit = {}) {
  const token = getToken();
  const headers: HeadersInit = { 'Content-Type': 'application/json', ...(init.headers || {}) };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(path, { ...init, headers });
  if (res.status === 401) clearToken();
  return res;
}

export const getReports = () => apiFetch('/api/reports');
export const getReport = (id: string) => apiFetch(`/api/reports/${id}`);
export const runPipeline = (body: {target: string; target_type: string}) => apiFetch('/api/pipeline/run', { method: 'POST', body: JSON.stringify(body)});
export const login = (body: {email: string; password: string}) => apiFetch('/api/auth/login', { method: 'POST', body: JSON.stringify(body)});
export const refresh = (refresh_token: string) => apiFetch('/api/auth/refresh', { method: 'POST', body: JSON.stringify({refresh_token})});
