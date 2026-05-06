import { AlertCircle, ArrowLeft, CheckCircle2, Mail, UserRound } from "lucide-react";
import { AIAnalysisPanel } from "./AIAnalysisPanel";
import { CategoryBadge } from "./CategoryBadge";
import { EmptyState } from "./EmptyState";
import { PriorityBadge } from "./PriorityBadge";
import { SourceBadge } from "./SourceBadge";
import { StatusBadge } from "./StatusBadge";
import { SimilarTicketsPanel } from "./SimilarTicketsPanel";
import { TicketActivityTimeline } from "./TicketActivityTimeline";
import { formatDateTime, isTicketOverdue } from "@/lib/sla";
import type { ApplyAnalysisPayload, TicketDetail } from "@/lib/types";

export function TicketDetailPanel({
  detail,
  analyzing,
  applyingAnalysis,
  onAnalyze,
  onApplyAnalysis,
  onCopyResponse,
  onOpenSimilarTicket,
  originTicket,
  onReturnToOrigin,
  onResolve,
}: {
  detail: TicketDetail | null;
  analyzing: boolean;
  applyingAnalysis: boolean;
  onAnalyze: (ticketId: number) => void;
  onApplyAnalysis: (ticketId: number, analysisId: number, payload: ApplyAnalysisPayload) => void;
  onCopyResponse: (text: string) => void;
  onOpenSimilarTicket: (ticketId: number) => void;
  originTicket: { id: number; title: string } | null;
  onReturnToOrigin: () => void;
  onResolve: () => void;
}) {
  if (!detail) {
    return (
      <aside className="rounded border border-slate-200 bg-white p-4 shadow-soft">
        <EmptyState title="Select a ticket." message="Ticket details, actions, and activity history will appear here." />
      </aside>
    );
  }

  const { ticket } = detail;
  const overdue = isTicketOverdue(ticket);

  return (
    <aside className="space-y-4 rounded border border-slate-200 bg-white p-4 shadow-soft lg:sticky lg:top-4 lg:max-h-[calc(100vh-9rem)] lg:overflow-auto">
      {originTicket && originTicket.id !== ticket.id ? (
        <button
          type="button"
          onClick={onReturnToOrigin}
          className="inline-flex w-full items-center justify-center gap-2 rounded border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
          title={`Return to ${originTicket.title}`}
        >
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          Back to {originTicket.title}
        </button>
      ) : null}

      <div>
        <div className="flex flex-wrap gap-2">
          <PriorityBadge priority={ticket.priority} />
          <StatusBadge status={ticket.status} />
          <CategoryBadge category={ticket.category} />
          <SourceBadge source={ticket.source} />
        </div>
        <h2 className="mt-3 text-lg font-semibold text-slate-950">{ticket.title}</h2>
        <p className="mt-2 text-sm leading-6 text-slate-600">{ticket.description}</p>
      </div>

      <div className="grid grid-cols-1 gap-3 border-y border-slate-200 py-4 text-sm sm:grid-cols-2">
        <div className="flex items-center gap-2 text-slate-700">
          <UserRound className="h-4 w-4 text-slate-400" aria-hidden="true" />
          <span>{ticket.customer_name}</span>
        </div>
        <div className="flex items-center gap-2 text-slate-700">
          <Mail className="h-4 w-4 text-slate-400" aria-hidden="true" />
          <span className="min-w-0 truncate">{ticket.customer_email}</span>
        </div>
        <div>Team: {ticket.assigned_team}</div>
        <div className={overdue ? "font-semibold text-red-700" : undefined}>
          Due: {formatDateTime(ticket.due_at)}
        </div>
        <div>Created: {formatDateTime(ticket.created_at)}</div>
        <div>Updated: {formatDateTime(ticket.updated_at)}</div>
      </div>

      {overdue ? (
        <div className="flex items-start gap-2 rounded border border-red-200 bg-red-50 p-3 text-sm text-red-800">
          <AlertCircle className="mt-0.5 h-4 w-4 flex-none" aria-hidden="true" />
          <span>This ticket is overdue and still needs action.</span>
        </div>
      ) : null}

      <div className="space-y-2 rounded border border-slate-200 bg-slate-50 p-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h3 className="text-sm font-semibold text-slate-950">Resolution</h3>
          <button
            type="button"
            onClick={onResolve}
            className="inline-flex items-center justify-center gap-2 rounded bg-blue-700 px-3 py-2 text-sm font-medium text-white hover:bg-blue-800"
          >
            <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
            {ticket.status === "resolved" ? "Update Resolution" : "Resolve Ticket"}
          </button>
        </div>
        {ticket.resolution_notes ? (
          <p className="text-sm leading-6 text-slate-700">{ticket.resolution_notes}</p>
        ) : (
          <p className="text-sm text-slate-500">No resolution notes saved yet.</p>
        )}
      </div>

      <AIAnalysisPanel
        analysis={detail.latest_analysis}
        running={analyzing}
        applying={applyingAnalysis}
        onAnalyze={() => onAnalyze(ticket.id)}
        onApply={(payload) => {
          if (detail.latest_analysis) {
            onApplyAnalysis(ticket.id, detail.latest_analysis.id, payload);
          }
        }}
        onCopy={onCopyResponse}
      />

      <SimilarTicketsPanel matches={detail.similar_ticket_matches} onOpenTicket={onOpenSimilarTicket} />

      <section>
        <h3 className="mb-3 text-sm font-semibold text-slate-950">Activity Timeline</h3>
        <TicketActivityTimeline events={detail.events} />
      </section>
    </aside>
  );
}
