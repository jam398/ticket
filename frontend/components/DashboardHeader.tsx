import { Plus, RefreshCcw, Search } from "lucide-react";

export function DashboardHeader({
  search,
  onSearchChange,
  onNewTicket,
  onRefresh,
}: {
  search: string;
  onSearchChange: (value: string) => void;
  onNewTicket: () => void;
  onRefresh: () => void;
}) {
  return (
    <header className="border-b border-line bg-white">
      <div className="mx-auto flex max-w-[1600px] flex-col gap-4 px-4 py-4 lg:flex-row lg:items-center lg:justify-between lg:px-6">
        <div className="min-w-0">
          <h1 className="text-xl font-semibold tracking-normal text-slate-950">TriagePilot AI</h1>
          <p className="mt-1 text-sm text-slate-600">
            AI-assisted ticket classification, routing, and response suggestions
          </p>
        </div>
        <div className="flex w-full flex-col gap-2 sm:flex-row lg:w-auto">
          <label className="relative min-w-0 flex-1 lg:w-80">
            <span className="sr-only">Search tickets</span>
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              value={search}
              onChange={(event) => onSearchChange(event.target.value)}
              className="h-10 w-full rounded border border-slate-300 bg-white pl-9 pr-3 text-sm text-slate-900"
              placeholder="Search tickets"
            />
          </label>
          <button
            type="button"
            onClick={onRefresh}
            className="inline-flex h-10 items-center justify-center gap-2 rounded border border-slate-300 bg-white px-3 text-sm font-medium text-slate-700 hover:bg-slate-50"
            title="Refresh dashboard"
          >
            <RefreshCcw className="h-4 w-4" aria-hidden="true" />
            <span>Refresh</span>
          </button>
          <button
            type="button"
            onClick={onNewTicket}
            className="inline-flex h-10 items-center justify-center gap-2 rounded bg-slate-900 px-3 text-sm font-medium text-white hover:bg-slate-800"
            title="Create new ticket"
          >
            <Plus className="h-4 w-4" aria-hidden="true" />
            <span>New Ticket</span>
          </button>
        </div>
      </div>
    </header>
  );
}
