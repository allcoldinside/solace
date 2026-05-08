const TOKEN_KEY = 'solace_token';
const REFRESH_KEY = 'solace_refresh';

export const saveTokens = (access: string, refresh: string) => {
  localStorage.setItem(TOKEN_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
};
export const saveToken = (t: string) => localStorage.setItem(TOKEN_KEY, t);
export const clearToken = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
};
export const getToken = () => localStorage.getItem(TOKEN_KEY);
export const getRefreshToken = () => localStorage.getItem(REFRESH_KEY);

async function tryRefresh(): Promise<boolean> {
  const rt = getRefreshToken();
  if (!rt) return false;
  const res = await fetch('/api/auth/refresh', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: rt }),
  });
  if (!res.ok) { clearToken(); return false; }
  const data = await res.json();
  saveTokens(data.access_token, data.refresh_token);
  return true;
}

export async function apiFetch(path: string, init: RequestInit = {}, retry = true): Promise<Response> {
  const token = getToken();
  const headers: Record<string, string> = { 'Content-Type': 'application/json', ...(init.headers as Record<string, string> || {}) };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(path, { ...init, headers });
  if (res.status === 401 && retry) {
    const ok = await tryRefresh();
    if (ok) return apiFetch(path, init, false);
    clearToken();
  }
  return res;
}

export const login = async (body: { email: string; password: string }) => {
  const res = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (res.ok) {
    const data = await res.json();
    saveTokens(data.access_token, data.refresh_token);
  }
  return res;
};

export const refresh = (refresh_token: string) =>
  apiFetch('/api/auth/refresh', { method: 'POST', body: JSON.stringify({ refresh_token }) });

export const getMe = () => apiFetch('/api/auth/me');
export const logout = (refresh_token: string) =>
  apiFetch('/api/auth/logout', { method: 'POST', body: JSON.stringify({ refresh_token }) });

export const getReports = () => apiFetch('/api/reports');
export const getReport = (id: string) => apiFetch(`/api/reports/${id}`);

export const runPipeline = (body: { target: string; target_type: string }) =>
  apiFetch('/api/pipeline/run', { method: 'POST', body: JSON.stringify(body) });

export const getPanel = () => apiFetch('/api/panel');
export const getPanelSession = (sessionId: string) => apiFetch(`/api/panel/${sessionId}`);

export const getCases = () => apiFetch('/api/cases');
export const getCase = (id: string) => apiFetch(`/api/cases/${id}`);
export const createCase = (body: { title: string; description?: string }) =>
  apiFetch('/api/cases', { method: 'POST', body: JSON.stringify(body) });

export const getWatches = () => apiFetch('/api/watches');
export const getWatch = (id: string) => apiFetch(`/api/watches/${id}`);
export const createWatch = (body: { target: string; target_type: string }) =>
  apiFetch('/api/watches', { method: 'POST', body: JSON.stringify(body) });

export const getEntities = () => apiFetch('/api/entities');
export const searchAPI = (q: string) => apiFetch(`/api/search?q=${encodeURIComponent(q)}`);
export const getMemory = () => apiFetch('/api/memory');
export const getGraph = () => apiFetch('/api/graph');
export const getHealth = () => fetch('/api/health');
export const getSystemInfo = () => apiFetch('/api/system/info');
