from app.models import Ticket
from app.schemas import encode_tags
from app.services.prompt_builder import build_triage_prompt


def test_prompt_builder_includes_ticket_context_schema_rules_and_no_history_warning():
    ticket = Ticket(
        title="Duplicate billing charge",
        description="The customer was charged twice for the monthly subscription.",
        customer_name="Avery Stone",
        customer_email="avery@example.com",
        tags=encode_tags(["billing", "payment"]),
    )

    prompt = build_triage_prompt(ticket)

    assert "Duplicate billing charge" in prompt
    assert "charged twice" in prompt
    assert "summary, category, priority, assigned_team" in prompt
    assert "No similar past tickets were found" in prompt
    assert "account_access" in prompt
    assert "urgent" in prompt
    assert "Use the provided customer name" in prompt
    assert "Do not address the user as \"Customer\"" in prompt
    assert "Make recommended_action resolution-first" in prompt
    assert "recommended_action must be exactly 5 numbered lines" in prompt
    assert "1. Verify:" in prompt
    assert "5. Close:" in prompt
    assert "we are investigating" in prompt
    assert "Do not ask the customer to confirm something by default" in prompt
    assert "password reset attempts" in prompt
    assert "Make recommended_action's Confirm line proof-oriented" in prompt
    assert "Avoid weak Confirm lines" in prompt
    assert "include both the ID and title" in prompt
    assert "Do not cite only bare ticket IDs" in prompt
    assert "never say \"escalate to engineering\"" in prompt
    assert "please confirm whether the issue also happens" not in prompt
    assert "routing this to Engineering" not in prompt
    assert "Route to Engineering" not in prompt


def test_prompt_builder_includes_supplied_similar_ticket_context():
    ticket = Ticket(
        title="Invoice missing",
        description="Customer needs the latest invoice.",
        customer_name="Avery Stone",
        customer_email="avery@example.com",
    )

    prompt = build_triage_prompt(ticket, ["Solved ticket #12: sent invoice from billing portal."])

    assert "Solved ticket #12" in prompt
    assert "No similar past tickets were found" not in prompt
    assert "Use similar solved ticket context and resolution notes as a playbook" in prompt
    assert "Category playbooks:" in prompt
