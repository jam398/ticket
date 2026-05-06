import type {
  AssignedTeam,
  TicketCategory,
  TicketPriority,
  TicketSource,
  TicketStatus,
} from "./types";

export const STATUS_OPTIONS: Array<{ value: TicketStatus; label: string }> = [
  { value: "open", label: "Open" },
  { value: "in_review", label: "In Review" },
  { value: "waiting_for_customer", label: "Waiting for Customer" },
  { value: "resolved", label: "Resolved" },
  { value: "closed", label: "Closed" },
];

export const PRIORITY_OPTIONS: Array<{ value: TicketPriority; label: string }> = [
  { value: "urgent", label: "Urgent" },
  { value: "high", label: "High" },
  { value: "medium", label: "Medium" },
  { value: "low", label: "Low" },
];

export const CATEGORY_OPTIONS: Array<{ value: TicketCategory; label: string }> = [
  { value: "account_access", label: "Account Access" },
  { value: "billing", label: "Billing" },
  { value: "technical_issue", label: "Technical Issue" },
  { value: "bug_report", label: "Bug Report" },
  { value: "feature_request", label: "Feature Request" },
  { value: "general_question", label: "General Question" },
  { value: "urgent_incident", label: "Urgent Incident" },
];

export const TEAM_OPTIONS: Array<{ value: AssignedTeam; label: string }> = [
  { value: "support", label: "Support" },
  { value: "billing", label: "Billing" },
  { value: "engineering", label: "Engineering" },
  { value: "product", label: "Product" },
  { value: "security", label: "Security" },
  { value: "operations", label: "Operations" },
];

export const SOURCE_OPTIONS: Array<{ value: TicketSource; label: string }> = [
  { value: "email", label: "Email" },
  { value: "web_form", label: "Web Form" },
  { value: "chat", label: "Chat" },
  { value: "phone", label: "Phone" },
  { value: "api", label: "API" },
];

export const SORT_OPTIONS = [
  { value: "newest", label: "Newest" },
  { value: "priority", label: "Priority" },
  { value: "status", label: "Status" },
  { value: "category", label: "Category" },
  { value: "overdue", label: "Overdue" },
] as const;

export function labelFor<T extends string>(options: Array<{ value: T; label: string }>, value: T): string {
  return options.find((option) => option.value === value)?.label ?? value;
}
