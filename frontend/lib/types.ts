export type TicketStatus = "open" | "in_review" | "waiting_for_customer" | "resolved" | "closed";
export type TicketCategory =
  | "account_access"
  | "billing"
  | "technical_issue"
  | "bug_report"
  | "feature_request"
  | "general_question"
  | "urgent_incident";
export type TicketPriority = "low" | "medium" | "high" | "urgent";
export type AssignedTeam = "support" | "billing" | "engineering" | "product" | "security" | "operations";
export type TicketSource = "email" | "web_form" | "chat" | "phone" | "api";

export type Ticket = {
  id: number;
  title: string;
  description: string;
  customer_name: string;
  customer_email: string;
  source: TicketSource;
  status: TicketStatus;
  category: TicketCategory;
  priority: TicketPriority;
  assigned_team: AssignedTeam;
  tags: string[];
  due_at: string | null;
  created_at: string;
  updated_at: string;
  resolved_at: string | null;
  resolution_notes: string | null;
};

export type TicketEvent = {
  id: number;
  ticket_id: number;
  event_type: string;
  message: string;
  created_at: string;
};

export type TicketAnalysis = {
  id: number;
  ticket_id: number;
  summary: string;
  category: TicketCategory;
  priority: TicketPriority;
  assigned_team: AssignedTeam;
  suggested_response: string;
  recommended_action: string;
  decision_reason: string;
  confidence_score: number;
  confidence_label: "High" | "Medium" | "Low";
  evidence: string[];
  warnings: string[];
  created_at: string;
};

export type SimilarTicketMatch = {
  id: number;
  ticket_id: number;
  matched_ticket_id: number;
  similarity_score: number;
  reason: string;
  created_at: string;
  matched_ticket: Ticket | null;
};

export type TicketDetail = {
  ticket: Ticket;
  latest_analysis: TicketAnalysis | null;
  similar_ticket_matches: SimilarTicketMatch[];
  events: TicketEvent[];
};

export type TicketListResponse = {
  items: Ticket[];
  total: number;
  page: number;
  page_size: number;
};

export type DashboardStats = {
  total_tickets: number;
  open: number;
  in_review: number;
  waiting_for_customer: number;
  resolved: number;
  closed: number;
  urgent: number;
  high: number;
  overdue: number;
  average_confidence_score: number;
};

export type TicketFilters = {
  status?: TicketStatus;
  category?: TicketCategory;
  priority?: TicketPriority;
  assigned_team?: AssignedTeam;
  source?: TicketSource;
  search?: string;
  sort?: "newest" | "priority" | "status" | "category" | "overdue";
};

export type NewTicketPayload = {
  title: string;
  description: string;
  customer_name: string;
  customer_email: string;
  source: TicketSource;
  tags: string[];
};

export type ResolveTicketPayload = {
  resolution_notes: string;
};

export type ApplyAnalysisPayload = {
  category?: TicketCategory;
  priority?: TicketPriority;
  assigned_team?: AssignedTeam;
};
