import pytest
from pydantic import ValidationError

from app.models import AssignedTeam, TicketCategory, TicketPriority
from app.schemas import AITriageOutput, confidence_label_for_score


def _valid_output() -> dict:
    return {
        "summary": "Customer cannot access account.",
        "category": "account_access",
        "priority": "high",
        "assigned_team": "support",
        "suggested_response": "We are checking the account access issue.",
        "recommended_action": "Verify login state and reset flow.",
        "decision_reason": "The ticket mentions login access.",
        "confidence_score": 0.86,
        "evidence": ["Title: Login issue"],
        "warnings": [],
    }


def test_ai_triage_output_validates_enums_score_and_text():
    output = AITriageOutput.model_validate(_valid_output())

    assert output.category == TicketCategory.ACCOUNT_ACCESS
    assert output.priority == TicketPriority.HIGH
    assert output.assigned_team == AssignedTeam.SUPPORT
    assert output.confidence_score == 0.86


def test_ai_triage_output_rejects_invalid_values():
    payload = _valid_output()
    payload["confidence_score"] = 1.2
    payload["summary"] = " "

    with pytest.raises(ValidationError):
        AITriageOutput.model_validate(payload)


def test_confidence_labels_are_stable():
    assert confidence_label_for_score(0.82) == "High"
    assert confidence_label_for_score(0.60) == "Medium"
    assert confidence_label_for_score(0.59) == "Low"
