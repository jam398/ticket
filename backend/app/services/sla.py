from datetime import datetime, timedelta

from app.models import Ticket, TicketPriority, TicketStatus, utc_now


SLA_HOURS: dict[TicketPriority | str, int] = {
    TicketPriority.URGENT: 1,
    TicketPriority.HIGH: 4,
    TicketPriority.MEDIUM: 24,
    TicketPriority.LOW: 72,
    "urgent": 1,
    "high": 4,
    "medium": 24,
    "low": 72,
}


def calculate_due_at(priority: TicketPriority | str, base_time: datetime | None = None) -> datetime:
    start = base_time or utc_now()
    return start + timedelta(hours=SLA_HOURS[priority])


def is_overdue(ticket: Ticket, now: datetime | None = None) -> bool:
    if ticket.status in {TicketStatus.RESOLVED, TicketStatus.CLOSED, "resolved", "closed"}:
        return False
    if ticket.due_at is None:
        return False
    return (now or utc_now()) > ticket.due_at
