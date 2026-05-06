from dataclasses import dataclass

from sqlalchemy import delete
from sqlmodel import Session

from app.models import SimilarTicketMatch, Ticket
from app.services.events import add_ticket_event
from app.services.vector_store import LocalChromaTicketStore, get_vector_store, ticket_document_text


@dataclass(frozen=True)
class SimilarTicketCandidate:
    ticket: Ticket
    similarity_score: float
    reason: str


def clear_ticket_index(vector_store: LocalChromaTicketStore | None = None) -> None:
    (vector_store or get_vector_store()).clear()


def index_ticket(ticket: Ticket, vector_store: LocalChromaTicketStore | None = None) -> None:
    (vector_store or get_vector_store()).upsert_ticket(ticket)


def index_tickets(tickets: list[Ticket], vector_store: LocalChromaTicketStore | None = None) -> None:
    (vector_store or get_vector_store()).upsert_tickets(tickets)


def retrieve_similar_tickets(
    session: Session,
    ticket: Ticket,
    limit: int = 5,
    vector_store: LocalChromaTicketStore | None = None,
) -> list[SimilarTicketCandidate]:
    matches = (vector_store or get_vector_store()).query(ticket, limit=limit)
    candidates: list[SimilarTicketCandidate] = []
    for match in matches:
        matched_ticket = session.get(Ticket, match.ticket_id)
        if matched_ticket is None:
            continue
        candidates.append(
            SimilarTicketCandidate(
                ticket=matched_ticket,
                similarity_score=match.similarity_score,
                reason=match.reason,
            )
        )
    return candidates


def persist_similar_matches(
    session: Session,
    ticket_id: int,
    candidates: list[SimilarTicketCandidate],
) -> list[SimilarTicketMatch]:
    session.execute(delete(SimilarTicketMatch).where(SimilarTicketMatch.ticket_id == ticket_id))
    persisted: list[SimilarTicketMatch] = []
    for candidate in candidates:
        match = SimilarTicketMatch(
            ticket_id=ticket_id,
            matched_ticket_id=candidate.ticket.id,
            similarity_score=candidate.similarity_score,
            reason=candidate.reason,
        )
        session.add(match)
        persisted.append(match)
    session.flush()
    return persisted


def similar_ticket_prompt_context(candidates: list[SimilarTicketCandidate]) -> list[str]:
    context: list[str] = []
    for candidate in candidates:
        context.append(
            f"Ticket #{candidate.ticket.id} ({candidate.similarity_score:.2f}): "
            f"{ticket_document_text(candidate.ticket)}"
        )
    return context


def add_similarity_event(session: Session, ticket_id: int, candidates: list[SimilarTicketCandidate]) -> None:
    if candidates:
        add_ticket_event(
            session,
            ticket_id,
            "similar_tickets_found",
            f"Found {len(candidates)} similar ticket(s) above the similarity threshold.",
        )
    else:
        add_ticket_event(
            session,
            ticket_id,
            "no_similar_tickets_found",
            "No similar past tickets met the similarity threshold.",
        )
