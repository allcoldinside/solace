/**
 * SOLACE API client – typed wrappers for all backend endpoints.
 * Tokens are stored in localStorage under "solace_access" / "solace_refresh".
 */

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api";

// ─── token helpers ──────────────────────────────────────────────────────────

function getAccessToken(): string | null {
  return localStorage.getItem("solace_access");
}

function setTokens(access: string, refresh: string): void {
  localStorage.setItem("solace_access", access);
  localStorage.setItem("solace_refresh", refresh);
}

function clearTokens(): void {
  localStorage.removeItem("solace_access");
  localStorage.removeItem("solace_refresh");
}

// ─── core fetch ─────────────────────────────────────────────────────────────

async function apiFetch<T>(
  path: string,
  init: RequestInit = {},
  authenticated = true,
): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(init.headers ?? {}),
  };

  if (authenticated) {
    const token = getAccessToken();
    if (token) {
      (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
    }
  }

  const res = await fetch(`${BASE_URL}${path}`, { ...init, headers });

  if (res.status === 401) {
    clearTokens();
    throw new Error("Unauthorized – please log in again.");
  }

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(String(body?.detail ?? res.statusText));
  }

  return res.json() as Promise<T>;
}

// ─── types ──────────────────────────────────────────────────────────────────

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface PipelineResponse {
  job_id: string;
  report_id: string;
  status: string;
  raw_count: number;
  enriched_count: number;
  entity_count: number;
  panel_session_id: string | null;
}

export interface ReportSummary {
  report_id: string;
  subject: string;
  classification: string;
  confidence: string;
  created_at: string;
}

export interface ReportDetail {
  report_id: string;
  subject: string;
  full_markdown: string;
  entity_map: Record<string, unknown>;
  source_log: Record<string, unknown>[];
}

export interface PanelSessionSummary {
  session_id: string;
  report_id: string;
  status: string;
  created_at: string;
}

export interface PanelSessionDetail {
  session_id: string;
  report_id: string;
  transcript: unknown[];
  synthesis: string;
}

export interface EntitySchema {
  entity_id: string;
  tenant_id: string;
  name: string;
  normalized_name: string;
  entity_type: string;
  confidence_score: number;
  attributes: Record<string, unknown>;
  source_report_ids: string[];
}

export interface CaseSummary {
  case_id: string;
  title: string;
  status: string;
  created_at: string;
}

export interface WatchSummary {
  watch_id: string;
  target: string;
  target_type: string;
  cadence: string;
  is_active: boolean;
}

export interface UserInfo {
  user_id: string;
  email: string;
  tenant_id: string;
  role: string;
}

// ─── auth ───────────────────────────────────────────────────────────────────

export async function login(email: string, password: string): Promise<TokenResponse> {
  const res = await apiFetch<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  }, false);
  setTokens(res.access_token, res.refresh_token);
  return res;
}

export async function register(
  email: string,
  password: string,
  tenant_id = "default",
  role = "analyst",
): Promise<TokenResponse> {
  const res = await apiFetch<TokenResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password, tenant_id, role }),
  }, false);
  setTokens(res.access_token, res.refresh_token);
  return res;
}

export async function refreshTokens(): Promise<TokenResponse> {
  const refresh_token = localStorage.getItem("solace_refresh");
  if (!refresh_token) throw new Error("No refresh token available.");
  const res = await apiFetch<TokenResponse>("/auth/refresh", {
    method: "POST",
    body: JSON.stringify({ refresh_token }),
  }, false);
  setTokens(res.access_token, res.refresh_token);
  return res;
}

export async function logout(refresh_token: string): Promise<void> {
  await apiFetch<{ message: string }>("/auth/logout", {
    method: "POST",
    body: JSON.stringify({ refresh_token }),
  });
  clearTokens();
}

export async function me(): Promise<UserInfo> {
  return apiFetch<UserInfo>("/auth/me");
}

// ─── pipeline ───────────────────────────────────────────────────────────────

export async function runPipeline(
  target: string,
  target_type = "unknown",
  tenant_id?: string,
): Promise<PipelineResponse> {
  return apiFetch<PipelineResponse>("/pipeline/run", {
    method: "POST",
    body: JSON.stringify({ target, target_type, tenant_id }),
  });
}

// ─── reports ────────────────────────────────────────────────────────────────

export async function listReports(): Promise<ReportSummary[]> {
  return apiFetch<ReportSummary[]>("/reports");
}

export async function getReport(report_id: string): Promise<ReportDetail> {
  return apiFetch<ReportDetail>(`/reports/${report_id}`);
}

// ─── panel sessions ─────────────────────────────────────────────────────────

export async function listPanelSessions(): Promise<PanelSessionSummary[]> {
  return apiFetch<PanelSessionSummary[]>("/panel");
}

export async function getPanelSession(session_id: string): Promise<PanelSessionDetail> {
  return apiFetch<PanelSessionDetail>(`/panel/${session_id}`);
}

// ─── entities ───────────────────────────────────────────────────────────────

export async function listEntities(): Promise<EntitySchema[]> {
  return apiFetch<EntitySchema[]>("/entities");
}

// ─── cases ──────────────────────────────────────────────────────────────────

export async function listCases(): Promise<CaseSummary[]> {
  return apiFetch<CaseSummary[]>("/cases");
}

export async function createCase(title: string, description = ""): Promise<CaseSummary> {
  return apiFetch<CaseSummary>("/cases", {
    method: "POST",
    body: JSON.stringify({ title, description }),
  });
}

// ─── watches ────────────────────────────────────────────────────────────────

export async function listWatches(): Promise<WatchSummary[]> {
  return apiFetch<WatchSummary[]>("/watches");
}

export async function createWatch(
  target: string,
  target_type = "unknown",
  cadence = "daily",
): Promise<WatchSummary> {
  return apiFetch<WatchSummary>("/watches", {
    method: "POST",
    body: JSON.stringify({ target, target_type, cadence }),
  });
}

// ─── search ─────────────────────────────────────────────────────────────────

export async function search(q: string, limit = 20): Promise<unknown[]> {
  return apiFetch<unknown[]>(`/search?q=${encodeURIComponent(q)}&limit=${limit}`);
}

// ─── graph ──────────────────────────────────────────────────────────────────

export async function getGraph(): Promise<unknown> {
  return apiFetch<unknown>("/graph");
}

// ─── memory ─────────────────────────────────────────────────────────────────

export async function listMemory(): Promise<unknown[]> {
  return apiFetch<unknown[]>("/memory");
}

// ─── health ─────────────────────────────────────────────────────────────────

export async function health(): Promise<{ status: string; service: string }> {
  return apiFetch<{ status: string; service: string }>("/health", {}, false);
}
