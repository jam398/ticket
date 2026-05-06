import { SlidersHorizontal } from "lucide-react";
import { TicketFilters } from "./TicketFilters";
import type { TicketFilters as TicketFiltersType } from "@/lib/types";

export function TicketQueueSidebar({
  filters,
  total,
  onChange,
  onClear,
}: {
  filters: TicketFiltersType;
  total: number;
  onChange: (key: keyof TicketFiltersType, value: string) => void;
  onClear: () => void;
}) {
  return (
    <aside className="rounded border border-slate-200 bg-white p-4 shadow-soft lg:sticky lg:top-4 lg:h-[calc(100vh-9rem)] lg:overflow-auto">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <h2 className="text-sm font-semibold text-slate-950">Queues</h2>
          <p className="mt-1 text-xs text-slate-500">{total} matching tickets</p>
        </div>
        <SlidersHorizontal className="h-4 w-4 text-slate-500" aria-hidden="true" />
      </div>
      <TicketFilters filters={filters} onChange={onChange} />
      <button
        type="button"
        onClick={onClear}
        className="mt-4 w-full rounded border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
      >
        Clear Filters
      </button>
    </aside>
  );
}
