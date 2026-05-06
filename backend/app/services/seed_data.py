import random
from datetime import datetime, timedelta

from sqlalchemy import delete
from sqlmodel import Session

from app.models import (
    AssignedTeam,
    SimilarTicketMatch,
    Ticket,
    TicketAnalysis,
    TicketCategory,
    TicketEvent,
    TicketPriority,
    TicketSource,
    TicketStatus,
    utc_now,
)
from app.schemas import encode_tags
from app.services.events import add_ticket_event
from app.services.rag import clear_ticket_index, index_tickets
from app.services.sla import calculate_due_at


CATEGORY_DISTRIBUTION = [
    (TicketCategory.ACCOUNT_ACCESS, 16),
    (TicketCategory.BILLING, 16),
    (TicketCategory.TECHNICAL_ISSUE, 18),
    (TicketCategory.BUG_REPORT, 16),
    (TicketCategory.FEATURE_REQUEST, 12),
    (TicketCategory.GENERAL_QUESTION, 10),
    (TicketCategory.URGENT_INCIDENT, 12),
]

PRIORITY_DISTRIBUTION = [
    (TicketPriority.LOW, 20),
    (TicketPriority.MEDIUM, 42),
    (TicketPriority.HIGH, 28),
    (TicketPriority.URGENT, 10),
]

STATUS_DISTRIBUTION = [
    (TicketStatus.OPEN, 25),
    (TicketStatus.IN_REVIEW, 20),
    (TicketStatus.WAITING_FOR_CUSTOMER, 15),
    (TicketStatus.RESOLVED, 25),
    (TicketStatus.CLOSED, 15),
]

SOURCE_DISTRIBUTION = [
    (TicketSource.EMAIL, 35),
    (TicketSource.WEB_FORM, 25),
    (TicketSource.CHAT, 20),
    (TicketSource.PHONE, 10),
    (TicketSource.API, 10),
]

CATEGORY_EXAMPLES: dict[TicketCategory, list[str]] = {
    TicketCategory.ACCOUNT_ACCESS: [
        "password reset email not received",
        "account locked after too many attempts",
        "MFA code not working",
        "verification link expired",
        "cannot access paid account",
        "login works on desktop but not mobile",
        "email changed and account access lost",
    ],
    TicketCategory.BILLING: [
        "duplicate charge on card",
        "refund request for cancelled plan",
        "payment method declined",
        "invoice not received",
        "subscription cancellation issue",
        "incorrect tax shown",
        "annual plan charged monthly",
    ],
    TicketCategory.TECHNICAL_ISSUE: [
        "dashboard not loading",
        "API timeout during sync",
        "file upload failing",
        "page returns 500 error",
        "integration disconnected",
        "slow report generation",
        "data sync stopped",
    ],
    TicketCategory.BUG_REPORT: [
        "save button not working",
        "wrong data displayed",
        "export file missing rows",
        "notification not sent",
        "form accepts invalid data",
        "date filter shows incorrect range",
        "UI freezes after save",
    ],
    TicketCategory.FEATURE_REQUEST: [
        "dark mode request",
        "export to CSV",
        "bulk edit tickets",
        "Slack integration",
        "dashboard analytics",
        "saved filters",
        "custom notification rules",
    ],
    TicketCategory.GENERAL_QUESTION: [
        "how to update profile",
        "where to find invoices",
        "how to invite team members",
        "what plan includes automation",
        "how to contact support",
        "how to change notification settings",
    ],
    TicketCategory.URGENT_INCIDENT: [
        "production system down",
        "customers cannot pay",
        "login outage",
        "data sync stopped for multiple clients",
        "suspected security alert",
        "checkout broken",
        "API unavailable for multiple clients",
    ],
}

TEAM_BY_CATEGORY = {
    TicketCategory.ACCOUNT_ACCESS: AssignedTeam.SUPPORT,
    TicketCategory.BILLING: AssignedTeam.BILLING,
    TicketCategory.TECHNICAL_ISSUE: AssignedTeam.ENGINEERING,
    TicketCategory.BUG_REPORT: AssignedTeam.ENGINEERING,
    TicketCategory.FEATURE_REQUEST: AssignedTeam.PRODUCT,
    TicketCategory.GENERAL_QUESTION: AssignedTeam.SUPPORT,
    TicketCategory.URGENT_INCIDENT: AssignedTeam.OPERATIONS,
}


def _expand_distribution(distribution: list[tuple[object, int]]) -> list[object]:
    values: list[object] = []
    for value, count in distribution:
        values.extend([value] * count)
    return values


def seed_database(session: Session) -> list[Ticket]:
    clear_ticket_index()
    for table in (SimilarTicketMatch, TicketAnalysis, TicketEvent, Ticket):
        session.execute(delete(table))
    session.commit()

    rng = random.Random(42)
    categories = _expand_distribution(CATEGORY_DISTRIBUTION)
    priorities = _expand_distribution(PRIORITY_DISTRIBUTION)
    statuses = _expand_distribution(STATUS_DISTRIBUTION)
    sources = _expand_distribution(SOURCE_DISTRIBUTION)
    for values in (categories, priorities, statuses, sources):
        rng.shuffle(values)

    now = utc_now()
    tickets: list[Ticket] = []

    for index in range(100):
        category = categories[index]
        priority = priorities[index]
        status = statuses[index]
        source = sources[index]
        example = CATEGORY_EXAMPLES[category][index % len(CATEGORY_EXAMPLES[category])]
        customer_number = index + 1
        created_at = now - timedelta(hours=index * 3)
        resolved = status in {TicketStatus.RESOLVED, TicketStatus.CLOSED}
        resolution_notes = None
        resolved_at = None
        if resolved:
            resolution_notes = (
                f"Reviewed the {example} case, confirmed the customer context, "
                "completed the required support action, and verified the customer could proceed."
            )
            resolved_at = created_at + timedelta(hours=6)

        ticket = Ticket(
            title=example.title(),
            description=(
                f"Customer reports {example}. The issue affects workspace "
                f"ACME-{customer_number:03d} and needs support follow-up."
            ),
            customer_name=f"Customer {customer_number}",
            customer_email=f"customer{customer_number}@example.com",
            source=source,
            status=status,
            category=category,
            priority=priority,
            assigned_team=TEAM_BY_CATEGORY[category],
            tags=encode_tags([category.value, source.value]),
            due_at=calculate_due_at(priority, created_at),
            created_at=created_at,
            updated_at=resolved_at or created_at,
            resolved_at=resolved_at,
            resolution_notes=resolution_notes,
        )
        session.add(ticket)
        session.flush()
        add_ticket_event(session, ticket.id, "ticket_created", "Ticket created from seed data.")
        if resolved:
            add_ticket_event(session, ticket.id, "ticket_resolved", "Ticket resolved in seed data.")
        tickets.append(ticket)

    session.commit()
    for ticket in tickets:
        session.refresh(ticket)
    index_tickets(tickets)
    return tickets
