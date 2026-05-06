from datetime import datetime, timedelta

from app.models import Ticket, TicketPriority, TicketStatus
from app.services.sla import calculate_due_at, is_overdue


def test_calculate_due_at_uses_required_hour_rules():
    base = datetime(2026, 5, 5, 12, 0, 0)

    assert calculate_due_at(TicketPriority.URGENT, base) == base + timedelta(hours=1)
    assert calculate_due_at(TicketPriority.HIGH, base) == base + timedelta(hours=4)
    assert calculate_due_at(TicketPriority.MEDIUM, base) == base + timedelta(hours=24)
    assert calculate_due_at(TicketPriority.LOW, base) == base + timedelta(hours=72)


def test_is_overdue_ignores_resolved_and_closed_tickets():
    now = datetime(2026, 5, 5, 12, 0, 0)
    open_ticket = Ticket(
        title="Overdue",
        description="Past due ticket",
        customer_name="Customer",
        customer_email="customer@example.com",
        due_at=now - timedelta(minutes=1),
    )
    resolved_ticket = Ticket(
        title="Resolved",
        description="Resolved ticket",
        customer_name="Customer",
        customer_email="customer@example.com",
        status=TicketStatus.RESOLVED,
        due_at=now - timedelta(days=1),
    )

    assert is_overdue(open_ticket, now) is True
    assert is_overdue(resolved_ticket, now) is False


def test_is_overdue_handles_missing_and_future_due_dates():
    now = datetime(2026, 5, 5, 12, 0, 0)
    missing_due_at = Ticket(
        title="Missing due",
        description="No SLA due date",
        customer_name="Customer",
        customer_email="customer@example.com",
        due_at=None,
    )
    future_due_at = Ticket(
        title="Future due",
        description="Future SLA due date",
        customer_name="Customer",
        customer_email="customer@example.com",
        due_at=now + timedelta(minutes=1),
    )

    assert is_overdue(missing_due_at, now) is False
    assert is_overdue(future_due_at, now) is False


def test_dashboard_overdue_count_uses_unresolved_past_due_tickets(client, session):
    now = datetime.now()
    tickets = [
        Ticket(
            title="Open overdue",
            description="Past due open ticket",
            customer_name="Customer",
            customer_email="open-overdue@example.com",
            due_at=now - timedelta(hours=1),
        ),
        Ticket(
            title="Review overdue",
            description="Past due in-review ticket",
            customer_name="Customer",
            customer_email="review-overdue@example.com",
            status=TicketStatus.IN_REVIEW,
            due_at=now - timedelta(hours=2),
        ),
        Ticket(
            title="Resolved past due",
            description="Past due but resolved",
            customer_name="Customer",
            customer_email="resolved@example.com",
            status=TicketStatus.RESOLVED,
            due_at=now - timedelta(days=1),
        ),
        Ticket(
            title="Open future due",
            description="Not yet due",
            customer_name="Customer",
            customer_email="future@example.com",
            due_at=now + timedelta(days=1),
        ),
    ]
    session.add_all(tickets)
    session.commit()

    response = client.get("/api/dashboard/stats")

    assert response.status_code == 200
    assert response.json()["overdue"] == 2
