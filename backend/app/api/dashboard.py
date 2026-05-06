from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Ticket, TicketAnalysis, TicketPriority, TicketStatus
from app.schemas import DashboardStats
from app.services.sla import is_overdue


router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def dashboard_stats(session: Session = Depends(get_session)) -> DashboardStats:
    tickets = session.exec(select(Ticket)).all()
    analyses = session.exec(select(TicketAnalysis)).all()
    confidence_values = [analysis.confidence_score for analysis in analyses]
    average_confidence = (
        round(sum(confidence_values) / len(confidence_values), 2) if confidence_values else 0.0
    )

    return DashboardStats(
        total_tickets=len(tickets),
        open=sum(1 for ticket in tickets if ticket.status == TicketStatus.OPEN),
        in_review=sum(1 for ticket in tickets if ticket.status == TicketStatus.IN_REVIEW),
        waiting_for_customer=sum(
            1 for ticket in tickets if ticket.status == TicketStatus.WAITING_FOR_CUSTOMER
        ),
        resolved=sum(1 for ticket in tickets if ticket.status == TicketStatus.RESOLVED),
        closed=sum(1 for ticket in tickets if ticket.status == TicketStatus.CLOSED),
        urgent=sum(1 for ticket in tickets if ticket.priority == TicketPriority.URGENT),
        high=sum(1 for ticket in tickets if ticket.priority == TicketPriority.HIGH),
        overdue=sum(1 for ticket in tickets if is_overdue(ticket)),
        average_confidence_score=average_confidence,
    )
