from sqlmodel import Session, col, select

from app.models import SimilarTicketMatch, Ticket, TicketAnalysis, TicketEvent
from app.schemas import (
    SimilarTicketMatchRead,
    TicketAnalysisRead,
    TicketDetailRead,
    TicketEventRead,
    TicketRead,
    confidence_label_for_score,
    decode_tags,
)


def ticket_to_read(ticket: Ticket) -> TicketRead:
    return TicketRead(
        id=ticket.id,
        title=ticket.title,
        description=ticket.description,
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        source=ticket.source,
        status=ticket.status,
        category=ticket.category,
        priority=ticket.priority,
        assigned_team=ticket.assigned_team,
        tags=decode_tags(ticket.tags),
        due_at=ticket.due_at,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
        resolved_at=ticket.resolved_at,
        resolution_notes=ticket.resolution_notes,
    )


def analysis_to_read(analysis: TicketAnalysis | None) -> TicketAnalysisRead | None:
    if analysis is None:
        return None
    return TicketAnalysisRead(
        id=analysis.id,
        ticket_id=analysis.ticket_id,
        summary=analysis.summary,
        category=analysis.category,
        priority=analysis.priority,
        assigned_team=analysis.assigned_team,
        suggested_response=analysis.suggested_response,
        recommended_action=analysis.recommended_action,
        decision_reason=analysis.decision_reason,
        confidence_score=analysis.confidence_score,
        confidence_label=confidence_label_for_score(analysis.confidence_score),
        evidence=decode_tags(analysis.evidence),
        warnings=decode_tags(analysis.warnings),
        created_at=analysis.created_at,
    )


def ticket_detail_to_read(session: Session, ticket: Ticket) -> TicketDetailRead:
    latest_analysis = session.exec(
        select(TicketAnalysis)
        .where(TicketAnalysis.ticket_id == ticket.id)
        .order_by(col(TicketAnalysis.created_at).desc())
    ).first()
    matches = session.exec(
        select(SimilarTicketMatch).where(SimilarTicketMatch.ticket_id == ticket.id)
    ).all()
    events = session.exec(
        select(TicketEvent)
        .where(TicketEvent.ticket_id == ticket.id)
        .order_by(col(TicketEvent.created_at).asc())
    ).all()

    return TicketDetailRead(
        ticket=ticket_to_read(ticket),
        latest_analysis=analysis_to_read(latest_analysis),
        similar_ticket_matches=[_similar_match_to_read(session, match) for match in matches],
        events=[TicketEventRead.model_validate(event) for event in events],
    )


def _similar_match_to_read(session: Session, match: SimilarTicketMatch) -> SimilarTicketMatchRead:
    matched_ticket = session.get(Ticket, match.matched_ticket_id)
    return SimilarTicketMatchRead(
        id=match.id,
        ticket_id=match.ticket_id,
        matched_ticket_id=match.matched_ticket_id,
        similarity_score=match.similarity_score,
        reason=match.reason,
        created_at=match.created_at,
        matched_ticket=ticket_to_read(matched_ticket) if matched_ticket else None,
    )
