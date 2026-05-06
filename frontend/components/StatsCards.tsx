import { AlertCircle, CheckCircle2, Clock, Flame, Inbox } from "lucide-react";
import type { DashboardStats } from "@/lib/types";

const cards = [
  { key: "total_tickets", label: "Total Tickets", icon: Inbox },
  { key: "open", label: "Open Tickets", icon: Clock },
  { key: "urgent", label: "Urgent Tickets", icon: Flame },
  { key: "overdue", label: "Overdue Tickets", icon: AlertCircle },
  { key: "resolved", label: "Resolved Tickets", icon: CheckCircle2 },
] as const;

export function StatsCards({ stats }: { stats: DashboardStats | null }) {
  return (
    <section className="grid grid-cols-2 gap-3 lg:grid-cols-5">
      {cards.map((card) => {
        const Icon = card.icon;
        const activeWarning = card.key === "overdue" && stats !== null && stats.overdue > 0;
        return (
          <div
            key={card.key}
            className={`rounded border p-4 shadow-soft ${
              activeWarning ? "border-red-200 bg-red-50" : "border-slate-200 bg-white"
            }`}
          >
            <div className="flex items-center justify-between gap-3">
              <p className={`text-xs font-medium uppercase ${activeWarning ? "text-red-700" : "text-slate-500"}`}>
                {card.label}
              </p>
              <Icon className={`h-4 w-4 ${activeWarning ? "text-red-700" : "text-slate-500"}`} aria-hidden="true" />
            </div>
            <p className={`mt-3 text-2xl font-semibold ${activeWarning ? "text-red-800" : "text-slate-950"}`}>
              {stats ? stats[card.key] : "-"}
            </p>
          </div>
        );
      })}
    </section>
  );
}
