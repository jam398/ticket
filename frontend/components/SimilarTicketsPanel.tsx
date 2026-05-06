import { GitBranch } from "lucide-react";
import { CategoryBadge } from "./CategoryBadge";
import { EmptyState } from "./EmptyState";
import { PriorityBadge } from "./PriorityBadge";
import { StatusBadge } from "./StatusBadge";
import type { SimilarTicketMatch } from "@/lib/types";

export function SimilarTicketsPanel({
  matches,
  onOpenTicket,
}: {
  matches: SimilarTicketMatch[];
  onOpenTicket: (ticketId: number) => void;
}) {
  return (
    <section className="rounded border border-slate-200 bg-slate-50 p-3">
      <div className="mb-2 flex items-center gap-2">
        <GitBranch className="h-4 w-4 text-slate-500" aria-hidden="true" />
        <h3 className="text-sm font-semibold text-slate-950">Similar Solved Tickets</h3>
      </div>
      <p className="mb-3 text-xs leading-5 text-slate-500">
        These prior tickets are the historical matches used as AI context.
      </p>

      {matches.length === 0 ? (
        <EmptyState
          title="No similar past tickets found."
          message="Analysis can still run without historical matches."
        />
      ) : (
        <div className="space-y-3">
          {matches.map((match) => {
            const ticket = match.matched_ticket;
            return (
              <article key={match.id} className="rounded border border-slate-200 bg-white p-3">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="text-xs font-semibold uppercase text-slate-500">
                      Ticket #{match.matched_ticket_id}
                    </p>
                    <p className="mt-1 truncate text-sm font-semibold text-slate-950">
                      {ticket ? ticket.title : "Matched ticket"}
                    </p>
                    <p className="mt-1 text-xs text-slate-500">{match.reason}</p>
                  </div>
                  <span className="rounded border border-blue-200 bg-blue-50 px-2 py-1 text-xs font-semibold text-blue-700">
                    {Math.round(match.similarity_score * 100)}%
                  </span>
                </div>
                {ticket ? (
                  <>
                    <div className="mt-3 flex flex-wrap gap-2">
                      <PriorityBadge priority={ticket.priority} />
                      <StatusBadge status={ticket.status} />
                      <CategoryBadge category={ticket.category} />
                    </div>
                    {ticket.resolution_notes ? (
                      <p className="mt-3 text-sm leading-6 text-slate-600">{ticket.resolution_notes}</p>
                    ) : null}
                    <button
                      type="button"
                      onClick={() => onOpenTicket(match.matched_ticket_id)}
                      className="mt-3 inline-flex items-center justify-center rounded border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                    >
                      Open Solved Ticket
                    </button>
                  </>
                ) : null}
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}
