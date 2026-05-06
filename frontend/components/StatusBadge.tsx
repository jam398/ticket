import { labelFor, STATUS_OPTIONS } from "@/lib/constants";
import type { TicketStatus } from "@/lib/types";

const statusClasses: Record<TicketStatus, string> = {
  open: "border-blue-200 bg-blue-50 text-blue-800",
  in_review: "border-violet-200 bg-violet-50 text-violet-800",
  waiting_for_customer: "border-amber-200 bg-amber-50 text-amber-800",
  resolved: "border-emerald-200 bg-emerald-50 text-emerald-800",
  closed: "border-slate-200 bg-slate-100 text-slate-700",
};

export function StatusBadge({ status }: { status: TicketStatus }) {
  return (
    <span className={`inline-flex min-w-0 items-center rounded border px-2 py-1 text-xs font-medium ${statusClasses[status]}`}>
      {labelFor(STATUS_OPTIONS, status)}
    </span>
  );
}
