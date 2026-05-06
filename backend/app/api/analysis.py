from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlmodel import Session

from app.api.serializers import ticket_detail_to_read
from app.database import get_session
from app.models import Ticket, TicketAnalysis, utc_now
from app.models import AssignedTeam, TicketCategory, TicketPriority
from app.schemas import AnalysisApplyRequest, TicketDetailRead
from app.services.events import add_ticket_event, describe_field_change
from app.services.rag import (
    add_similarity_event,
    persist_similar_matches,
    retrieve_similar_tickets,
    similar_ticket_prompt_context,
)
from app.services.sla import calculate_due_at
from app.services.triage import analysis_model_from_output, analyze_ticket


router = APIRouter(prefix="/api/tickets", tags=["analysis"])


@router.post("/{ticket_id}/analyze", response_model=TicketDetailRead)
def analyze_ticket_endpoint(ticket_id: int, session: Session = Depends(get_session)) -> TicketDetailRead:
    ticket = session.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    try:
        similar_candidates = retrieve_similar_tickets(session, ticket)
        output = analyze_ticket(ticket, similar_ticket_prompt_context(similar_candidates))
    except ValidationError as exc:
        raise HTTPException(status_code=502, detail="AI triage output failed validation") from exc

    persist_similar_matches(session, ticket.id, similar_candidates)
    analysis = analysis_model_from_output(ticket.id, output)
    session.add(analysis)
    session.flush()
    add_similarity_event(session, ticket.id, similar_candidates)
    add_ticket_event(
        session,
        ticket.id,
        "ai_triage_generated",
        f"AI triage generated analysis #{analysis.id}.",
    )
    session.commit()
    session.refresh(ticket)
    return ticket_detail_to_read(session, ticket)


@router.post("/{ticket_id}/apply-analysis/{analysis_id}", response_model=TicketDetailRead)
def apply_analysis_endpoint(
    ticket_id: int,
    analysis_id: int,
    payload: AnalysisApplyRequest | None = None,
    session: Session = Depends(get_session),
) -> TicketDetailRead:
    ticket = session.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    analysis = session.get(TicketAnalysis, analysis_id)
    if analysis is None or analysis.ticket_id != ticket.id:
        raise HTTPException(status_code=404, detail="Analysis not found")

    category: TicketCategory = payload.category if payload and payload.category else analysis.category
    priority: TicketPriority = payload.priority if payload and payload.priority else analysis.priority
    assigned_team: AssignedTeam = (
        payload.assigned_team if payload and payload.assigned_team else analysis.assigned_team
    )

    changes: list[str] = []
    if ticket.category != category:
        changes.append(describe_field_change("Category", ticket.category, category))
        ticket.category = category
    if ticket.priority != priority:
        changes.append(describe_field_change("Priority", ticket.priority, priority))
        ticket.priority = priority
        ticket.due_at = calculate_due_at(ticket.priority)
    if ticket.assigned_team != assigned_team:
        changes.append(describe_field_change("Assigned team", ticket.assigned_team, assigned_team))
        ticket.assigned_team = assigned_team

    ticket.updated_at = utc_now()
    session.add(ticket)
    message = "AI suggestion applied."
    if changes:
        message = "AI suggestion applied: " + " ".join(changes)
    add_ticket_event(session, ticket.id, "ai_suggestion_applied", message)
    session.commit()
    session.refresh(ticket)
    return ticket_detail_to_read(session, ticket)
