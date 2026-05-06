from datetime import UTC, datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_REVIEW = "in_review"
    WAITING_FOR_CUSTOMER = "waiting_for_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketCategory(str, Enum):
    ACCOUNT_ACCESS = "account_access"
    BILLING = "billing"
    TECHNICAL_ISSUE = "technical_issue"
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    GENERAL_QUESTION = "general_question"
    URGENT_INCIDENT = "urgent_incident"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class AssignedTeam(str, Enum):
    SUPPORT = "support"
    BILLING = "billing"
    ENGINEERING = "engineering"
    PRODUCT = "product"
    SECURITY = "security"
    OPERATIONS = "operations"


class TicketSource(str, Enum):
    EMAIL = "email"
    WEB_FORM = "web_form"
    CHAT = "chat"
    PHONE = "phone"
    API = "api"


class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    customer_name: str
    customer_email: str = Field(index=True)
    source: TicketSource = Field(
        default=TicketSource.WEB_FORM,
        sa_column=Column(String, nullable=False, index=True),
    )
    status: TicketStatus = Field(
        default=TicketStatus.OPEN,
        sa_column=Column(String, nullable=False, index=True),
    )
    category: TicketCategory = Field(
        default=TicketCategory.GENERAL_QUESTION,
        sa_column=Column(String, nullable=False, index=True),
    )
    priority: TicketPriority = Field(
        default=TicketPriority.MEDIUM,
        sa_column=Column(String, nullable=False, index=True),
    )
    assigned_team: AssignedTeam = Field(
        default=AssignedTeam.SUPPORT,
        sa_column=Column(String, nullable=False, index=True),
    )
    tags: str = Field(default="[]")
    due_at: Optional[datetime] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=utc_now, index=True)
    updated_at: datetime = Field(default_factory=utc_now)
    resolved_at: Optional[datetime] = Field(default=None, index=True)
    resolution_notes: Optional[str] = None


class TicketAnalysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: int = Field(foreign_key="ticket.id", index=True)
    summary: str
    category: TicketCategory = Field(sa_column=Column(String, nullable=False))
    priority: TicketPriority = Field(sa_column=Column(String, nullable=False))
    assigned_team: AssignedTeam = Field(sa_column=Column(String, nullable=False))
    suggested_response: str
    recommended_action: str
    decision_reason: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    evidence: str = Field(default="[]")
    warnings: str = Field(default="[]")
    created_at: datetime = Field(default_factory=utc_now, index=True)


class SimilarTicketMatch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: int = Field(foreign_key="ticket.id", index=True)
    matched_ticket_id: int = Field(foreign_key="ticket.id", index=True)
    similarity_score: float = Field(ge=0.0, le=1.0)
    reason: str
    created_at: datetime = Field(default_factory=utc_now)


class TicketEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: int = Field(foreign_key="ticket.id", index=True)
    event_type: str = Field(index=True)
    message: str
    created_at: datetime = Field(default_factory=utc_now, index=True)
