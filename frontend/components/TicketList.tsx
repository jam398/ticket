import { EmptyState } from "./EmptyState";
import { LoadingState } from "./LoadingState";
import { TicketRow } from "./TicketRow";
import type { Ticket } from "@/lib/types";

export function TicketList({
  tickets,
  selectedTicketId,
  loading,
  onSelect,
}: {
  tickets: Ticket[];
  selectedTicketId: number | null;
  loading: boolean;
  onSelect: (ticket: Ticket) => void;
}) {
  if (loading) {
    return <LoadingState label="Loading tickets" />;
  }

  if (tickets.length === 0) {
    return (
      <EmptyState
        title="No tickets match this queue."
        message="Adjust the filters or create a new ticket to populate this view."
      />
    );
  }

  return (
    <section className="overflow-hidden rounded border border-slate-200 bg-white shadow-soft">
      <div className="border-b border-slate-200 px-4 py-3">
        <h2 className="text-sm font-semibold text-slate-950">Ticket List</h2>
      </div>
      <div>
        {tickets.map((ticket) => (
          <TicketRow
            key={ticket.id}
            ticket={ticket}
            selected={ticket.id === selectedTicketId}
            onSelect={() => onSelect(ticket)}
          />
        ))}
      </div>
    </section>
  );
}
