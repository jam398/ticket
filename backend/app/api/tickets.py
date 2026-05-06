from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlmodel import Session, col, select

from app.database import get_session
from app.api.serializers import ticket_detail_to_read, ticket_to_read
from app.models import (
    AssignedTeam,
    Ticket,
    TicketCategory,
    TicketPriority,
    TicketSource,
    TicketStatus,
    utc_now,
)
from app.schemas import (
    TicketCreate,
    TicketDetailRead,
    TicketListResponse,
    TicketRead,
    TicketResolveRequest,
    TicketUpdate,
    decode_tags,
    encode_tags,
)
from app.services.events import add_ticket_event, describe_field_change
from app.services.rag import index_ticket
from app.services.sla import calculate_due_at


router = APIRouter(prefix="/api/tickets", tags=["tickets"])


@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, session: Session = Depends(get_session)) -> TicketRead:
    now = utc_now()
    ticket = Ticket(
        title=payload.title,
        description=payload.description,
        customer_name=payload.customer_name,
        customer_email=payload.customer_email,
        source=payload.source,
        status=TicketStatus.OPEN,
        category=TicketCategory.GENERAL_QUESTION,
        priority=TicketPriority.MEDIUM,
        assigned_team=AssignedTeam.SUPPORT,
        tags=encode_tags(payload.tags),
        due_at=calculate_due_at(TicketPriority.MEDIUM, now),
        created_at=now,
        updated_at=now,
    )
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    add_ticket_event(session, ticket.id, "ticket_created", "Ticket created.")
    index_ticket(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket_to_read(ticket)


@router.get("", response_model=TicketListResponse)
def list_tickets(
    status_filter: TicketStatus | None = Query(default=None, alias="status"),
    category: TicketCategory | None = None,
    priority: TicketPriority | None = None,
    assigned_team: AssignedTeam | None = None,
    source: TicketSource | None = None,
    search: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    sort: str = "newest",
    session: Session = Depends(get_session),
) -> TicketListResponse:
    statement = select(Ticket)
    if status_filter is not None:
        statement = statement.where(Ticket.status == status_filter)
    if category is not None:
        statement = statement.where(Ticket.category == category)
    if priority is not None:
        statement = statement.where(Ticket.priority == priority)
    if assigned_team is not None:
        statement = statement.where(Ticket.assigned_team == assigned_team)
    if source is not None:
        statement = statement.where(Ticket.source == source)
    if search:
        pattern = f"%{search.strip()}%"
        statement = statement.where(
            or_(
                col(Ticket.title).like(pattern),
                col(Ticket.description).like(pattern),
                col(Ticket.customer_email).like(pattern),
            )
        )

    all_matches = session.exec(statement).all()
    if sort == "priority":
        all_matches = sorted(all_matches, key=lambda ticket: str(ticket.priority))
    elif sort == "status":
        all_matches = sorted(all_matches, key=lambda ticket: str(ticket.status))
    elif sort == "category":
        all_matches = sorted(all_matches, key=lambda ticket: str(ticket.category))
    elif sort == "overdue":
        all_matches = sorted(all_matches, key=lambda ticket: ticket.due_at or datetime.max)
    else:
        all_matches = sorted(all_matches, key=lambda ticket: ticket.created_at, reverse=True)

    start = (page - 1) * page_size
    end = start + page_size
    return TicketListResponse(
        items=[ticket_to_read(ticket) for ticket in all_matches[start:end]],
        total=len(all_matches),
        page=page,
        page_size=page_size,
    )


@router.get("/{ticket_id}", response_model=TicketDetailRead)
def get_ticket(ticket_id: int, session: Session = Depends(get_session)) -> TicketDetailRead:
    ticket = session.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket_detail_to_read(session, ticket)


@router.patch("/{ticket_id}/resolve", response_model=TicketDetailRead)
def resolve_ticket(
    ticket_id: int,
    payload: TicketResolveRequest,
    session: Session = Depends(get_session),
) -> TicketDetailRead:
    ticket = session.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    already_resolved = ticket.status == TicketStatus.RESOLVED
    now = utc_now()
    ticket.status = TicketStatus.RESOLVED
    ticket.resolved_at = ticket.resolved_at or now
    ticket.updated_at = now
    ticket.resolution_notes = payload.resolution_notes
    session.add(ticket)
    if already_resolved:
        add_ticket_event(session, ticket.id, "resolution_updated", "Resolution notes updated.")
    else:
        add_ticket_event(session, ticket.id, "ticket_resolved", "Ticket resolved with resolution notes.")
    session.commit()
    session.refresh(ticket)
    index_ticket(ticket)
    return ticket_detail_to_read(session, ticket)


@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket(
    ticket_id: int, payload: TicketUpdate, session: Session = Depends(get_session)
) -> TicketRead:
    ticket = session.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    changes: list[tuple[str, object, object]] = []
    update_data = payload.model_dump(exclude_unset=True)
    for field_name, value in update_data.items():
        if field_name == "tags":
            old_value = decode_tags(ticket.tags)
            ticket.tags = encode_tags(value)
            changes.append(("tags", old_value, value))
            continue
        old_value = getattr(ticket, field_name)
        if old_value != value:
            setattr(ticket, field_name, value)
            changes.append((field_name, old_value, value))

    if any(field_name == "priority" for field_name, _, _ in changes):
        ticket.due_at = calculate_due_at(ticket.priority)

    ticket.updated_at = utc_now()
    session.add(ticket)

    for field_name, old_value, new_value in changes:
        if field_name == "status":
            add_ticket_event(
                session,
                ticket.id,
                "status_changed",
                describe_field_change("Status", old_value, new_value),
            )
        elif field_name == "priority":
            add_ticket_event(
                session,
                ticket.id,
                "priority_changed",
                describe_field_change("Priority", old_value, new_value),
            )
        elif field_name == "assigned_team":
            add_ticket_event(
                session,
                ticket.id,
                "assigned_team_changed",
                describe_field_change("Assigned team", old_value, new_value),
            )

    session.commit()
    session.refresh(ticket)
    return ticket_to_read(ticket)
