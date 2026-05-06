import type { Ticket } from "./types";

export function isTicketOverdue(ticket: Ticket): boolean {
  return (
    !["resolved", "closed"].includes(ticket.status) &&
    ticket.due_at !== null &&
    new Date(ticket.due_at) < new Date()
  );
}

export function formatDateTime(value: string | null): string {
  if (!value) {
    return "Not set";
  }

  return new Intl.DateTimeFormat("en", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export function formatCompactDateTime(value: string | null): string {
  if (!value) {
    return "Not set";
  }

  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(value));
}
