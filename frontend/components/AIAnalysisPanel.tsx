import { useEffect, useState } from "react";
import { Bot, CheckCircle2, Copy, Sparkles, TriangleAlert } from "lucide-react";
import { CategoryBadge } from "./CategoryBadge";
import { EmptyState } from "./EmptyState";
import { PriorityBadge } from "./PriorityBadge";
import { StatusBadge } from "./StatusBadge";
import { CATEGORY_OPTIONS, PRIORITY_OPTIONS, TEAM_OPTIONS } from "@/lib/constants";
import type { ApplyAnalysisPayload, AssignedTeam, TicketAnalysis, TicketCategory, TicketPriority } from "@/lib/types";

function confidenceClass(label: TicketAnalysis["confidence_label"]) {
  if (label === "High") {
    return "border-emerald-200 bg-emerald-50 text-emerald-700";
  }
  if (label === "Medium") {
    return "border-amber-200 bg-amber-50 text-amber-700";
  }
  return "border-red-200 bg-red-50 text-red-700";
}

function numberedActionLines(text: string) {
  return text
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => line.replace(/^\d+\.\s*/, ""))
    .filter(Boolean);
}

export function AIAnalysisPanel({
  analysis,
  running,
  applying,
  onAnalyze,
  onApply,
  onCopy,
}: {
  analysis: TicketAnalysis | null;
  running: boolean;
  applying: boolean;
  onAnalyze: () => void;
  onApply: (payload: ApplyAnalysisPayload) => void;
  onCopy: (text: string) => void;
}) {
  const [category, setCategory] = useState<TicketCategory | "">("");
  const [priority, setPriority] = useState<TicketPriority | "">("");
  const [assignedTeam, setAssignedTeam] = useState<AssignedTeam | "">("");

  useEffect(() => {
    setCategory(analysis?.category ?? "");
    setPriority(analysis?.priority ?? "");
    setAssignedTeam(analysis?.assigned_team ?? "");
  }, [analysis]);

  return (
    <section className="rounded border border-slate-200 bg-slate-50 p-3">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <Bot className="h-4 w-4 text-slate-500" aria-hidden="true" />
          <h3 className="text-sm font-semibold text-slate-950">AI Analysis</h3>
        </div>
        <button
          type="button"
          onClick={onAnalyze}
          disabled={running || applying}
          className="inline-flex items-center justify-center gap-2 rounded bg-slate-900 px-3 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-500"
        >
          <Sparkles className="h-4 w-4" aria-hidden="true" />
          {running ? "Running" : analysis ? "Run Again" : "Run AI Triage"}
        </button>
      </div>

      {!analysis ? (
        <EmptyState
          title="No AI analysis yet."
          message="Run AI Triage to generate a structured recommendation before applying any changes."
        />
      ) : (
        <div className="space-y-3">
          <div className="flex flex-wrap gap-2">
            <CategoryBadge category={analysis.category} />
            <PriorityBadge priority={analysis.priority} />
            <StatusBadge status="in_review" />
            <span
              className={`inline-flex items-center rounded border px-2 py-1 text-xs font-semibold ${confidenceClass(
                analysis.confidence_label,
              )}`}
            >
              {analysis.confidence_label} confidence ({Math.round(analysis.confidence_score * 100)}%)
            </span>
          </div>

          <div className="grid grid-cols-1 gap-3 rounded border border-slate-200 bg-white p-3 sm:grid-cols-3">
            <p className="text-xs leading-5 text-slate-500 sm:col-span-3">
              Apply updates only these triage fields: category, priority, and team.
            </p>
            <label className="block">
              <span className="text-xs font-semibold uppercase text-slate-500">Category</span>
              <select
                value={category}
                onChange={(event) => setCategory(event.target.value as TicketCategory)}
                className="mt-1 h-9 w-full rounded border border-slate-300 bg-white px-2 text-sm text-slate-900"
              >
                {CATEGORY_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>
            <label className="block">
              <span className="text-xs font-semibold uppercase text-slate-500">Priority</span>
              <select
                value={priority}
                onChange={(event) => setPriority(event.target.value as TicketPriority)}
                className="mt-1 h-9 w-full rounded border border-slate-300 bg-white px-2 text-sm text-slate-900"
              >
                {PRIORITY_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>
            <label className="block">
              <span className="text-xs font-semibold uppercase text-slate-500">Team</span>
              <select
                value={assignedTeam}
                onChange={(event) => setAssignedTeam(event.target.value as AssignedTeam)}
                className="mt-1 h-9 w-full rounded border border-slate-300 bg-white px-2 text-sm text-slate-900"
              >
                {TEAM_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div>
            <p className="text-sm font-semibold text-slate-950">{analysis.summary}</p>
            <p className="mt-1 text-sm leading-6 text-slate-600">{analysis.decision_reason}</p>
          </div>

          <div className="rounded border border-slate-200 bg-white p-3">
            <p className="text-xs font-semibold uppercase text-slate-500">Suggested Response</p>
            <p className="mt-2 text-sm leading-6 text-slate-700">{analysis.suggested_response}</p>
          </div>

          <div className="rounded border border-slate-200 bg-white p-3">
            <p className="text-xs font-semibold uppercase text-slate-500">Recommended Action</p>
            {numberedActionLines(analysis.recommended_action).length > 1 ? (
              <ol className="mt-2 list-decimal space-y-2 pl-5 text-sm leading-6 text-slate-700">
                {numberedActionLines(analysis.recommended_action).map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ol>
            ) : (
              <p className="mt-2 whitespace-pre-line text-sm leading-6 text-slate-700">
                {analysis.recommended_action}
              </p>
            )}
          </div>

          {analysis.evidence.length > 0 ? (
            <div>
              <p className="text-xs font-semibold uppercase text-slate-500">Evidence</p>
              <p className="mt-1 text-xs leading-5 text-slate-500">
                Ticket numbers refer to prior solved matches listed in Similar Solved Tickets.
              </p>
              <ul className="mt-2 space-y-1 text-sm text-slate-700">
                {analysis.evidence.map((item) => (
                  <li key={item}>- {item}</li>
                ))}
              </ul>
            </div>
          ) : null}

          {analysis.warnings.length > 0 ? (
            <div className="space-y-2">
              {analysis.warnings.map((warning) => (
                <div key={warning} className="flex items-start gap-2 rounded border border-amber-200 bg-amber-50 p-2 text-sm text-amber-800">
                  <TriangleAlert className="mt-0.5 h-4 w-4 flex-none" aria-hidden="true" />
                  <span>{warning}</span>
                </div>
              ))}
            </div>
          ) : null}

          <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
            <button
              type="button"
              onClick={() => onCopy(analysis.suggested_response)}
              className="inline-flex items-center justify-center gap-2 rounded border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
            >
              <Copy className="h-4 w-4" aria-hidden="true" />
              Copy Response
            </button>
            <button
              type="button"
              onClick={() =>
                onApply({
                  category: category || undefined,
                  priority: priority || undefined,
                  assigned_team: assignedTeam || undefined,
                })
              }
              disabled={running || applying}
              title="Updates category, priority, and team only"
              className="inline-flex items-center justify-center gap-2 rounded bg-blue-700 px-3 py-2 text-sm font-medium text-white hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-blue-400"
            >
              <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
              {applying ? "Applying Fields" : "Apply Triage Fields"}
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
