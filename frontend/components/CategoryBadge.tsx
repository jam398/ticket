import { CATEGORY_OPTIONS, labelFor } from "@/lib/constants";
import type { TicketCategory } from "@/lib/types";

export function CategoryBadge({ category }: { category: TicketCategory }) {
  return (
    <span className="inline-flex min-w-0 items-center rounded border border-slate-200 bg-white px-2 py-1 text-xs font-medium text-slate-700">
      {labelFor(CATEGORY_OPTIONS, category)}
    </span>
  );
}
