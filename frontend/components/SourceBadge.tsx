import { labelFor, SOURCE_OPTIONS } from "@/lib/constants";
import type { TicketSource } from "@/lib/types";

export function SourceBadge({ source }: { source: TicketSource }) {
  return (
    <span className="inline-flex min-w-0 items-center rounded border border-slate-200 bg-slate-50 px-2 py-1 text-xs font-medium text-slate-700">
      {labelFor(SOURCE_OPTIONS, source)}
    </span>
  );
}
