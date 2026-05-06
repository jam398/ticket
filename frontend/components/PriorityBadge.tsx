import { labelFor, PRIORITY_OPTIONS } from "@/lib/constants";
import type { TicketPriority } from "@/lib/types";

const priorityClasses: Record<TicketPriority, string> = {
  urgent: "border-red-200 bg-red-50 text-red-800",
  high: "border-orange-200 bg-orange-50 text-orange-800",
  medium: "border-sky-200 bg-sky-50 text-sky-800",
  low: "border-emerald-200 bg-emerald-50 text-emerald-800",
};

export function PriorityBadge({ priority }: { priority: TicketPriority }) {
  return (
    <span className={`inline-flex min-w-0 items-center rounded border px-2 py-1 text-xs font-medium ${priorityClasses[priority]}`}>
      {labelFor(PRIORITY_OPTIONS, priority)}
    </span>
  );
}
