import {
  CATEGORY_OPTIONS,
  PRIORITY_OPTIONS,
  SORT_OPTIONS,
  SOURCE_OPTIONS,
  STATUS_OPTIONS,
  TEAM_OPTIONS,
} from "@/lib/constants";
import type { TicketFilters as TicketFiltersType } from "@/lib/types";

type FilterKey = keyof TicketFiltersType;

function FilterSelect({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: string;
  options: Array<{ value: string; label: string }>;
  onChange: (value: string) => void;
}) {
  return (
    <label className="block">
      <span className="text-xs font-medium uppercase text-slate-500">{label}</span>
      <select
        aria-label={label}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="mt-1 h-9 w-full rounded border border-slate-300 bg-white px-2 text-sm text-slate-900"
      >
        <option value="">All</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

export function TicketFilters({
  filters,
  onChange,
}: {
  filters: TicketFiltersType;
  onChange: (key: FilterKey, value: string) => void;
}) {
  return (
    <div className="space-y-4">
      <FilterSelect
        label="Status"
        value={filters.status ?? ""}
        options={STATUS_OPTIONS}
        onChange={(value) => onChange("status", value)}
      />
      <FilterSelect
        label="Priority"
        value={filters.priority ?? ""}
        options={PRIORITY_OPTIONS}
        onChange={(value) => onChange("priority", value)}
      />
      <FilterSelect
        label="Category"
        value={filters.category ?? ""}
        options={CATEGORY_OPTIONS}
        onChange={(value) => onChange("category", value)}
      />
      <FilterSelect
        label="Team"
        value={filters.assigned_team ?? ""}
        options={TEAM_OPTIONS}
        onChange={(value) => onChange("assigned_team", value)}
      />
      <FilterSelect
        label="Source"
        value={filters.source ?? ""}
        options={SOURCE_OPTIONS}
        onChange={(value) => onChange("source", value)}
      />
      <FilterSelect
        label="Sort"
        value={filters.sort ?? "newest"}
        options={[...SORT_OPTIONS]}
        onChange={(value) => onChange("sort", value)}
      />
    </div>
  );
}
