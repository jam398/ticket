import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.config import get_settings
from app.models import Ticket, TicketStatus
from app.services.embeddings import overlap_score


DOMAIN_KEYWORDS = {
    "billing",
    "charge",
    "charged",
    "invoice",
    "refund",
    "payment",
    "password",
    "login",
    "mfa",
    "error",
    "sync",
    "upload",
    "outage",
    "checkout",
    "security",
}


@dataclass(frozen=True)
class VectorMatch:
    ticket_id: int
    similarity_score: float
    reason: str


def ticket_document_text(ticket: Ticket) -> str:
    resolution = f" Resolution: {ticket.resolution_notes}" if ticket.resolution_notes else ""
    return (
        f"{ticket.title}. {ticket.description}. "
        f"Category: {ticket.category}. Priority: {ticket.priority}. "
        f"Status: {ticket.status}.{resolution}"
    )


def _value(value: object) -> str:
    return str(getattr(value, "value", value))


class LocalChromaTicketStore:
    """Small persistent vector-store fallback used when ChromaDB is unavailable in local tests."""

    def __init__(self, storage_path: str | None = None) -> None:
        configured_path = Path(storage_path or get_settings().chroma_path)
        self.storage_dir = configured_path
        self.storage_file = configured_path / "ticket_documents.json"
        self._documents: dict[str, dict[str, Any]] = {}
        self._load()

    def clear(self) -> None:
        self._documents = {}
        self._persist()

    def count(self) -> int:
        return len(self._documents)

    def upsert_ticket(self, ticket: Ticket) -> None:
        if ticket.id is None:
            return
        self._documents[str(ticket.id)] = {
            "ticket_id": ticket.id,
            "text": ticket_document_text(ticket),
                "metadata": {
                    "category": _value(ticket.category),
                    "priority": _value(ticket.priority),
                    "status": _value(ticket.status),
                    "has_resolution": bool(ticket.resolution_notes),
                },
            }
        self._persist()

    def upsert_tickets(self, tickets: list[Ticket]) -> None:
        for ticket in tickets:
            if ticket.id is not None:
                self._documents[str(ticket.id)] = {
                    "ticket_id": ticket.id,
                    "text": ticket_document_text(ticket),
                    "metadata": {
                        "category": _value(ticket.category),
                        "priority": _value(ticket.priority),
                        "status": _value(ticket.status),
                        "has_resolution": bool(ticket.resolution_notes),
                    },
                }
        self._persist()

    def query(self, ticket: Ticket, limit: int = 5, threshold: float | None = None) -> list[VectorMatch]:
        threshold = threshold if threshold is not None else get_settings().similarity_threshold
        query_text = ticket_document_text(ticket)
        query_keywords = {keyword for keyword in DOMAIN_KEYWORDS if keyword in query_text.lower()}
        matches: list[VectorMatch] = []
        for raw_id, document in self._documents.items():
            ticket_id = int(raw_id)
            if ticket.id is not None and ticket_id == ticket.id:
                continue
            score = overlap_score(query_text, document["text"])
            document_keywords = {keyword for keyword in DOMAIN_KEYWORDS if keyword in document["text"].lower()}
            metadata = document.get("metadata", {})
            solved = metadata.get("status") in {TicketStatus.RESOLVED.value, TicketStatus.CLOSED.value} and metadata.get(
                "has_resolution"
            )
            if _value(ticket.category) == metadata.get("category"):
                score += 0.08
            if query_keywords & document_keywords:
                score += 0.25
            if solved:
                score += 0.30
            score = min(round(score, 3), 0.99)
            if score >= threshold:
                reason = "Semantic overlap"
                if solved:
                    reason += " with solved-ticket resolution context"
                matches.append(VectorMatch(ticket_id=ticket_id, similarity_score=score, reason=reason))

        return sorted(matches, key=lambda match: match.similarity_score, reverse=True)[:limit]

    def _load(self) -> None:
        if not self.storage_file.exists():
            self._documents = {}
            return
        try:
            self._documents = json.loads(self.storage_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            self._documents = {}

    def _persist(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.storage_file.write_text(json.dumps(self._documents, indent=2), encoding="utf-8")


def get_vector_store() -> LocalChromaTicketStore:
    return LocalChromaTicketStore()
