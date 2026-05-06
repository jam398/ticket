from sqlmodel import Session

from app.models import TicketEvent


def format_event_value(value: object) -> str:
    raw_value = getattr(value, "value", value)
    return str(raw_value).replace("_", " ").title()


def describe_field_change(field_label: str, old_value: object, new_value: object) -> str:
    return (
        f"{field_label} changed from {format_event_value(old_value)} "
        f"to {format_event_value(new_value)}."
    )


def add_ticket_event(session: Session, ticket_id: int, event_type: str, message: str) -> TicketEvent:
    if not message.strip():
        raise ValueError("Ticket event message must not be empty")
    event = TicketEvent(ticket_id=ticket_id, event_type=event_type, message=message)
    session.add(event)
    return event
