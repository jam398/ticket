import { AlertCircle } from "lucide-react";
import { CategoryBadge } from "./CategoryBadge";
import { PriorityBadge } from "./PriorityBadge";
import { SourceBadge } from "./SourceBadge";
import { StatusBadge } from "./StatusBadge";
import { formatCompactDateTime, isTicketOverdue } from "@/lib/sla";
import type { Ticket } from "@/lib/types";

export function TicketRow({
  ticket,
  selected,
  onSelect,
}: {
  ticket: Ticket;
  selected: boolean;
  onSelect: () => void;
}) {
  const overdue = isTicketOverdue(ticket);

  return (
    <button
      type="button"
      onClick={onSelect}
      className={`w-full border-b border-slate-200 p-4 text-left hover:bg-slate-50 ${
        selected ? "bg-blue-50" : "bg-white"
      }`}
    >
      <div className="flex flex-col gap-3 xl:flex-row xl:items-start xl:justify-between">
        <div className="min-w-0 flex-1">
          <div className="flex min-w-0 items-center gap-2">
            <h3 className="truncate text-sm font-semibold text-slate-950">{ticket.title}</h3>
            {overdue ? (
              <span className="inline-flex flex-none items-center gap-1 rounded border border-red-200 bg-red-50 px-2 py-0.5 text-xs font-semibold text-red-700">
                <AlertCircle className="h-3.5 w-3.5" aria-hidden="true" />
                Overdue
              </span>
            ) : null}
          </div>
          <p className="mt-1 line-clamp-2 text-sm leading-6 text-slate-600">{ticket.description}</p>
          <p className="mt-2 text-xs text-slate-500">{ticket.customer_email}</p>
        </div>
        <div className="flex flex-wrap gap-2 xl:max-w-xs xl:justify-end">
          <PriorityBadge priority={ticket.priority} />
          <StatusBadge status={ticket.status} />
          <CategoryBadge category={ticket.category} />
          <SourceBadge source={ticket.source} />
        </div>
      </div>
      <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500">
        <span>Team: {ticket.assigned_team}</span>
        <span className={overdue ? "font-semibold text-red-700" : undefined}>
          Due: {formatCompactDateTime(ticket.due_at)}
        </span>
        <span>Created: {formatCompactDateTime(ticket.created_at)}</span>
      </div>
    </button>
  );
}
