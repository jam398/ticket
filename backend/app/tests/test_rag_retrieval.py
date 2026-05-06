from sqlmodel import select

from app.models import AssignedTeam, Ticket, TicketCategory, TicketPriority, TicketStatus
from app.services.rag import index_tickets, retrieve_similar_tickets
from app.services.vector_store import LocalChromaTicketStore


def test_retrieve_similar_tickets_prefers_solved_ticket_with_resolution(session, tmp_path):
    solved = Ticket(
        title="Duplicate charge on card",
        description="Customer reports a duplicate charge on the subscription card.",
        customer_name="Solved Customer",
        customer_email="solved@example.com",
        status=TicketStatus.RESOLVED,
        category=TicketCategory.BILLING,
        priority=TicketPriority.HIGH,
        assigned_team=AssignedTeam.BILLING,
        resolution_notes="Refunded the duplicate card charge and confirmed the corrected invoice.",
    )
    open_ticket = Ticket(
        title="Duplicate charge pending review",
        description="Customer reports a duplicate charge but it is not resolved yet.",
        customer_name="Open Customer",
        customer_email="open@example.com",
        category=TicketCategory.BILLING,
        priority=TicketPriority.HIGH,
        assigned_team=AssignedTeam.BILLING,
    )
    query_ticket = Ticket(
        title="Duplicate billing charge",
        description="The customer was charged twice for a subscription.",
        customer_name="Query Customer",
        customer_email="query@example.com",
        category=TicketCategory.BILLING,
        priority=TicketPriority.HIGH,
        assigned_team=AssignedTeam.BILLING,
    )
    session.add_all([solved, open_ticket, query_ticket])
    session.commit()
    for ticket in (solved, open_ticket, query_ticket):
        session.refresh(ticket)

    store = LocalChromaTicketStore(str(tmp_path))
    store.clear()
    index_tickets([solved, open_ticket, query_ticket], store)

    matches = retrieve_similar_tickets(session, query_ticket, vector_store=store)

    assert matches
    assert matches[0].ticket.id == solved.id
    assert matches[0].similarity_score >= 0.70
    assert "solved-ticket" in matches[0].reason


def test_retrieve_similar_tickets_ignores_low_similarity(session, tmp_path):
    indexed = Ticket(
        title="Password reset email missing",
        description="Customer cannot receive the password reset email.",
        customer_name="Indexed Customer",
        customer_email="indexed@example.com",
        category=TicketCategory.ACCOUNT_ACCESS,
    )
    query_ticket = Ticket(
        title="Dark mode dashboard request",
        description="Customer wants theme controls for the dashboard.",
        customer_name="Query Customer",
        customer_email="query@example.com",
        category=TicketCategory.FEATURE_REQUEST,
    )
    session.add_all([indexed, query_ticket])
    session.commit()
    session.refresh(indexed)
    session.refresh(query_ticket)

    store = LocalChromaTicketStore(str(tmp_path))
    store.clear()
    index_tickets([indexed, query_ticket], store)

    assert retrieve_similar_tickets(session, query_ticket, vector_store=store) == []


def test_analyze_endpoint_persists_similar_matches_and_event(client, session):
    solved = Ticket(
        title="Duplicate charge on card",
        description="Customer reports a duplicate charge on the subscription card.",
        customer_name="Solved Customer",
        customer_email="solved@example.com",
        status=TicketStatus.RESOLVED,
        category=TicketCategory.BILLING,
        priority=TicketPriority.HIGH,
        assigned_team=AssignedTeam.BILLING,
        resolution_notes="Refunded the duplicate card charge and confirmed the corrected invoice.",
    )
    session.add(solved)
    session.commit()
    session.refresh(solved)

    store = LocalChromaTicketStore()
    store.clear()
    index_tickets([solved], store)

    response = client.post(
        "/api/tickets",
        json={
            "title": "Duplicate billing charge",
            "description": "The customer was charged twice for the monthly subscription.",
            "customer_name": "RAG Customer",
            "customer_email": "rag@example.com",
            "source": "email",
            "tags": ["billing"],
        },
    )
    assert response.status_code == 201
    ticket_id = response.json()["id"]

    detail = client.post(f"/api/tickets/{ticket_id}/analyze").json()

    assert detail["similar_ticket_matches"]
    assert detail["similar_ticket_matches"][0]["matched_ticket"]["resolution_notes"]
    assert "similar_tickets_found" in [event["event_type"] for event in detail["events"]]
    assert "No similar past tickets were found" not in detail["latest_analysis"]["warnings"]

    stored_matches = session.exec(select(Ticket).where(Ticket.id == solved.id)).all()
    assert stored_matches
