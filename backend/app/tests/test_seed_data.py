from collections import Counter

from sqlmodel import select

from app.models import Ticket, TicketStatus
from app.services.seed_data import seed_database
from app.services.vector_store import get_vector_store


def test_seed_database_creates_100_realistic_tickets(session):
    tickets = seed_database(session)

    assert len(tickets) == 100

    persisted = session.exec(select(Ticket)).all()
    assert len(persisted) == 100

    categories = Counter(ticket.category for ticket in persisted)
    priorities = Counter(ticket.priority for ticket in persisted)
    statuses = Counter(ticket.status for ticket in persisted)
    sources = Counter(ticket.source for ticket in persisted)

    assert set(categories) == {
        "account_access",
        "billing",
        "technical_issue",
        "bug_report",
        "feature_request",
        "general_question",
        "urgent_incident",
    }
    assert priorities["urgent"] == 10
    assert statuses["resolved"] == 25
    assert statuses["closed"] == 15
    assert sources["email"] == 35

    resolved_or_closed = [
        ticket
        for ticket in persisted
        if ticket.status in {TicketStatus.RESOLVED, TicketStatus.CLOSED, "resolved", "closed"}
    ]
    assert resolved_or_closed
    assert all(ticket.resolution_notes for ticket in resolved_or_closed)
    assert get_vector_store().count() == 100
