from app.models import AssignedTeam, TicketCategory, TicketPriority
from app.schemas import AITriageOutput


def test_ai_output_accepts_provider_string_evidence_and_empty_warning():
    output = AITriageOutput.model_validate(
        {
            "summary": "Customer cannot load the dashboard.",
            "category": "technical_issue",
            "priority": "high",
            "assigned_team": "support",
            "suggested_response": "Thanks for reporting this. We are checking the dashboard loading issue.",
            "recommended_action": "Verify the workspace, browser state, and recent dashboard errors before sending a workaround.",
            "decision_reason": "The ticket describes a dashboard loading failure.",
            "confidence_score": 0.85,
            "evidence": "Description says the dashboard is not loading for workspace ACME-001.",
            "warnings": "",
        }
    )

    assert output.evidence == ["Description says the dashboard is not loading for workspace ACME-001."]
    assert output.warnings == []


def test_ai_output_normalizes_common_provider_enum_and_confidence_variants():
    output = AITriageOutput.model_validate(
        {
            "summary": "Customer was charged twice.",
            "category": "Billing",
            "priority": "Critical",
            "assigned_team": "Billing Team",
            "suggested_response": "Thanks for reporting this. Billing will review the duplicate charge.",
            "recommended_action": "Verify the invoice and refund eligibility, then document the billing correction.",
            "decision_reason": "The ticket describes a duplicate billing charge.",
            "confidence_score": "92%",
            "evidence": ["Title mentions duplicate billing charge."],
            "warnings": None,
        }
    )

    assert output.category == TicketCategory.BILLING
    assert output.priority == TicketPriority.URGENT
    assert output.assigned_team == AssignedTeam.BILLING
    assert output.confidence_score == 0.92
    assert output.warnings == []


def test_ai_output_normalizes_provider_evidence_object():
    output = AITriageOutput.model_validate(
        {
            "summary": "Customer needs login help.",
            "category": "Account Access Issue",
            "priority": "Normal",
            "assigned_team": "Customer Support Team",
            "suggested_response": "Thanks for contacting support. We will help restore account access.",
            "recommended_action": "Verify identity, check account state, and reset access if the customer passes verification.",
            "decision_reason": "The ticket mentions login and account access.",
            "confidence_score": 85,
            "evidence": {"title": "Cannot login", "description": "MFA code is not accepted"},
            "warnings": [],
        }
    )

    assert output.category == TicketCategory.ACCOUNT_ACCESS
    assert output.priority == TicketPriority.MEDIUM
    assert output.assigned_team == AssignedTeam.SUPPORT
    assert output.confidence_score == 0.85
    assert "title: Cannot login" in output.evidence
