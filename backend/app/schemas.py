import json
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import AssignedTeam, TicketCategory, TicketPriority, TicketSource, TicketStatus


def _normalize_token(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _normalize_enum_value(value: object, allowed_values: set[str], aliases: dict[str, str]) -> object:
    if not isinstance(value, str):
        return value
    token = _normalize_token(value)
    if token in allowed_values:
        return token
    return aliases.get(token, value)


def _coerce_text_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        cleaned = value.strip()
        return [cleaned] if cleaned else []
    if isinstance(value, dict):
        return [f"{key}: {item}".strip() for key, item in value.items() if str(item).strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()] if str(value).strip() else []


def _non_empty(value: str) -> str:
    if not value or not value.strip():
        raise ValueError("value must not be empty")
    return value.strip()


def decode_tags(raw_tags: str | None) -> list[str]:
    if not raw_tags:
        return []
    try:
        parsed = json.loads(raw_tags)
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, list):
        return []
    return [str(tag) for tag in parsed]


def encode_tags(tags: list[str] | None) -> str:
    return json.dumps(tags or [])


def confidence_label_for_score(score: float) -> str:
    if score >= 0.8:
        return "High"
    if score >= 0.6:
        return "Medium"
    return "Low"


class TicketCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    customer_name: str = Field(min_length=1)
    customer_email: str = Field(min_length=1)
    source: TicketSource = TicketSource.WEB_FORM
    tags: list[str] = Field(default_factory=list)

    @field_validator("title", "description", "customer_name", "customer_email")
    @classmethod
    def required_text(cls, value: str) -> str:
        return _non_empty(value)


class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    category: Optional[TicketCategory] = None
    priority: Optional[TicketPriority] = None
    assigned_team: Optional[AssignedTeam] = None
    source: Optional[TicketSource] = None
    tags: Optional[list[str]] = None
    resolution_notes: Optional[str] = None


class TicketResolveRequest(BaseModel):
    resolution_notes: str = Field(min_length=1)

    @field_validator("resolution_notes")
    @classmethod
    def required_notes(cls, value: str) -> str:
        return _non_empty(value)


class AnalysisApplyRequest(BaseModel):
    category: Optional[TicketCategory] = None
    priority: Optional[TicketPriority] = None
    assigned_team: Optional[AssignedTeam] = None


class TicketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    customer_name: str
    customer_email: str
    source: TicketSource
    status: TicketStatus
    category: TicketCategory
    priority: TicketPriority
    assigned_team: AssignedTeam
    tags: list[str]
    due_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
    resolution_notes: Optional[str]


class TicketAnalysisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_id: int
    summary: str
    category: TicketCategory
    priority: TicketPriority
    assigned_team: AssignedTeam
    suggested_response: str
    recommended_action: str
    decision_reason: str
    confidence_score: float
    confidence_label: str
    evidence: list[str]
    warnings: list[str]
    created_at: datetime


class AITriageOutput(BaseModel):
    summary: str = Field(min_length=1)
    category: TicketCategory
    priority: TicketPriority
    assigned_team: AssignedTeam
    suggested_response: str = Field(min_length=1)
    recommended_action: str = Field(min_length=1)
    decision_reason: str = Field(min_length=1)
    confidence_score: float = Field(ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, value: object) -> object:
        return _normalize_enum_value(
            value,
            {item.value for item in TicketCategory},
            {
                "account": TicketCategory.ACCOUNT_ACCESS.value,
                "account_access_issue": TicketCategory.ACCOUNT_ACCESS.value,
                "access": TicketCategory.ACCOUNT_ACCESS.value,
                "bug": TicketCategory.BUG_REPORT.value,
                "feature": TicketCategory.FEATURE_REQUEST.value,
                "feature_request_issue": TicketCategory.FEATURE_REQUEST.value,
                "general": TicketCategory.GENERAL_QUESTION.value,
                "question": TicketCategory.GENERAL_QUESTION.value,
                "technical": TicketCategory.TECHNICAL_ISSUE.value,
                "technical_support": TicketCategory.TECHNICAL_ISSUE.value,
                "urgent": TicketCategory.URGENT_INCIDENT.value,
                "incident": TicketCategory.URGENT_INCIDENT.value,
            },
        )

    @field_validator("priority", mode="before")
    @classmethod
    def normalize_priority(cls, value: object) -> object:
        return _normalize_enum_value(
            value,
            {item.value for item in TicketPriority},
            {
                "critical": TicketPriority.URGENT.value,
                "emergency": TicketPriority.URGENT.value,
                "normal": TicketPriority.MEDIUM.value,
                "standard": TicketPriority.MEDIUM.value,
            },
        )

    @field_validator("assigned_team", mode="before")
    @classmethod
    def normalize_assigned_team(cls, value: object) -> object:
        return _normalize_enum_value(
            value,
            {item.value for item in AssignedTeam},
            {
                "billing_team": AssignedTeam.BILLING.value,
                "customer_support": AssignedTeam.SUPPORT.value,
                "customer_support_team": AssignedTeam.SUPPORT.value,
                "engineering_team": AssignedTeam.ENGINEERING.value,
                "product_team": AssignedTeam.PRODUCT.value,
                "security_team": AssignedTeam.SECURITY.value,
                "support_team": AssignedTeam.SUPPORT.value,
                "technical_support": AssignedTeam.SUPPORT.value,
                "technical_support_team": AssignedTeam.SUPPORT.value,
                "operations_team": AssignedTeam.OPERATIONS.value,
            },
        )

    @field_validator("confidence_score", mode="before")
    @classmethod
    def normalize_confidence_score(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            if value.endswith("%"):
                value = value[:-1]
                parsed = float(value)
                return parsed / 100
            return float(value)
        if isinstance(value, (int, float)) and value > 1 and value <= 100:
            return value / 100
        return value

    @field_validator(
        "summary",
        "suggested_response",
        "recommended_action",
        "decision_reason",
    )
    @classmethod
    def required_text(cls, value: str) -> str:
        return _non_empty(value)

    @field_validator("evidence", "warnings", mode="before")
    @classmethod
    def normalize_text_list(cls, value: object) -> list[str]:
        return _coerce_text_list(value)

    @field_validator("evidence", "warnings")
    @classmethod
    def clean_text_list(cls, values: list[str]) -> list[str]:
        return [item.strip() for item in values if item.strip()]


class SimilarTicketMatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_id: int
    matched_ticket_id: int
    similarity_score: float
    reason: str
    created_at: datetime
    matched_ticket: Optional[TicketRead] = None


class TicketEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_id: int
    event_type: str
    message: str
    created_at: datetime


class TicketDetailRead(BaseModel):
    ticket: TicketRead
    latest_analysis: Optional[TicketAnalysisRead]
    similar_ticket_matches: list[SimilarTicketMatchRead]
    events: list[TicketEventRead]


class TicketListResponse(BaseModel):
    items: list[TicketRead]
    total: int
    page: int
    page_size: int


class DashboardStats(BaseModel):
    total_tickets: int
    open: int
    in_review: int
    waiting_for_customer: int
    resolved: int
    closed: int
    urgent: int
    high: int
    overdue: int
    average_confidence_score: float
