import type {
  ApplyAnalysisPayload,
  DashboardStats,
  NewTicketPayload,
  ResolveTicketPayload,
  TicketDetail,
  TicketFilters,
  TicketListResponse,
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with ${response.status}`);
  }

  return (await response.json()) as T;
}

export function fetchDashboardStats(): Promise<DashboardStats> {
  return request<DashboardStats>("/api/dashboard/stats");
}

export function fetchTickets(filters: TicketFilters): Promise<TicketListResponse> {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value) {
      params.set(key, value);
    }
  });
  params.set("page_size", "100");
  const query = params.toString();
  return request<TicketListResponse>(`/api/tickets${query ? `?${query}` : ""}`);
}

export function fetchTicketDetail(ticketId: number): Promise<TicketDetail> {
  return request<TicketDetail>(`/api/tickets/${ticketId}`);
}

export function createTicket(payload: NewTicketPayload): Promise<TicketDetail["ticket"]> {
  return request<TicketDetail["ticket"]>("/api/tickets", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function analyzeTicket(ticketId: number): Promise<TicketDetail> {
  return request<TicketDetail>(`/api/tickets/${ticketId}/analyze`, {
    method: "POST",
  });
}

export function applyAnalysis(
  ticketId: number,
  analysisId: number,
  payload?: ApplyAnalysisPayload,
): Promise<TicketDetail> {
  return request<TicketDetail>(`/api/tickets/${ticketId}/apply-analysis/${analysisId}`, {
    method: "POST",
    body: JSON.stringify(payload ?? {}),
  });
}

export function resolveTicket(ticketId: number, payload: ResolveTicketPayload): Promise<TicketDetail> {
  return request<TicketDetail>(`/api/tickets/${ticketId}/resolve`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}
