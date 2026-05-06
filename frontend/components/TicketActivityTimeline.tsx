import { EmptyState } from "./EmptyState";
import { formatCompactDateTime } from "@/lib/sla";
import type { TicketEvent } from "@/lib/types";

function formatEventType(value: string) {
  return value.replaceAll("_", " ");
}

export function TicketActivityTimeline({ events }: { events: TicketEvent[] }) {
  if (events.length === 0) {
    return <EmptyState title="No activity yet." message="Ticket events will appear here as work happens." />;
  }

  return (
    <div className="space-y-3">
      {events.map((event) => (
        <div key={event.id} className="border-l-2 border-slate-200 pl-3">
          <p className="text-sm font-medium text-slate-900">{event.message}</p>
          <p className="mt-1 text-xs capitalize text-slate-500">
            {formatEventType(event.event_type)} - {formatCompactDateTime(event.created_at)}
          </p>
        </div>
      ))}
    </div>
  );
}
