from app.models import AssignedTeam, Ticket, TicketCategory, TicketPriority
from app.schemas import encode_tags
from app.services.triage import analyze_ticket, triage_quality_findings


def _ticket() -> Ticket:
    return Ticket(
        title="Dashboard Not Loading",
        description="Customer reports dashboard not loading. The issue affects workspace ACME-001.",
        customer_name="Avery Stone",
        customer_email="avery@example.com",
        tags=encode_tags(["technical_issue"]),
    )


def _output(recommended_action: str, suggested_response: str = "We will verify the workspace and retry the dashboard.") -> dict:
    return {
        "summary": "Avery Stone cannot load the dashboard for workspace ACME-001.",
        "category": TicketCategory.TECHNICAL_ISSUE.value,
        "priority": TicketPriority.HIGH.value,
        "assigned_team": AssignedTeam.ENGINEERING.value,
        "suggested_response": suggested_response,
        "recommended_action": recommended_action,
        "decision_reason": "The ticket describes a dashboard loading failure.",
        "confidence_score": 0.86,
        "evidence": ["Title: Dashboard Not Loading"],
        "warnings": [],
    }


def _good_action() -> str:
    return "\n".join(
        [
            "1. Verify: Confirm workspace ACME-001 is affected and the dashboard fails after refresh.",
            "2. Inspect: Check browser console, network errors, backend logs, and similar solved tickets.",
            "3. Try: Apply a matching workaround or have the customer retry after cache/session refresh.",
            "4. Confirm: The dashboard loads successfully or the same failure is reproduced with evidence.",
            "5. Close: Save the workaround; create a defect only if the issue remains reproducible.",
        ]
    )


def test_triage_quality_finds_routing_and_action_shape_drift():
    output = analyze_ticket(
        _ticket(),
        ai_client=_StaticClient(
            _output(
                "Verify the workspace and escalate internally.",
                "We will investigate and route this to the right team.",
            )
        ),
    )

    assert output.warnings == ["AI quality guardrail rewrote response/action text to remove drift."]
    assert not triage_quality_findings(output)
    combined = f"{output.suggested_response}\n{output.recommended_action}".lower()
    assert "escalate" not in combined
    assert "route" not in combined
    assert "we will investigate" not in combined


def test_analyze_ticket_retries_before_using_repaired_output():
    client = _RepairingClient()

    output = analyze_ticket(_ticket(), ai_client=client)

    assert client.call_count == 2
    assert "failed these quality checks" in client.second_prompt
    assert output.suggested_response == "We will verify workspace ACME-001, inspect dashboard errors, and try a cache/session refresh workaround before asking for extra browser details."
    assert output.recommended_action == _good_action()


def test_triage_quality_rejects_customer_confirmation_for_internal_records():
    output = analyze_ticket(
        _ticket(),
        ai_client=_StaticClient(
            _output(
                _good_action(),
                "We will verify your account lock status. Please confirm if you received password reset emails or lockout notifications.",
            )
        ),
    )

    combined = f"{output.suggested_response}\n{output.recommended_action}".lower()
    assert "password reset emails" not in combined
    assert "lockout notifications" not in combined
    assert "please confirm" not in combined
    assert not triage_quality_findings(output)


def test_triage_quality_allows_precise_external_detail_request():
    output = analyze_ticket(
        _ticket(),
        ai_client=_StaticClient(
            _output(
                _good_action(),
                "We will reproduce the dashboard issue and inspect workspace ACME-001 logs; please provide the exact error message and browser if the failure only appears on your device.",
            )
        ),
    )

    assert "exact error message and browser" in output.suggested_response
    assert not triage_quality_findings(output)


def test_triage_quality_rejects_customer_work_confirm_line():
    output = analyze_ticket(
        _ticket(),
        ai_client=_StaticClient(
            _output(
                "\n".join(
                    [
                        "1. Verify: Confirm workspace ACME-001 is affected and the dashboard fails after refresh.",
                        "2. Inspect: Check browser console, network errors, backend logs, and similar solved tickets.",
                        "3. Try: Apply the matching workaround from similar solved tickets.",
                        "4. Confirm: Ask the customer if the dashboard now loads correctly.",
                        "5. Close: Save the workaround; create a defect only if the issue remains reproducible.",
                    ]
                )
            )
        ),
    )

    assert "ask the customer" not in output.recommended_action.lower()
    assert not triage_quality_findings(output)


def test_triage_quality_rejects_weak_confirm_line_without_proof():
    output = analyze_ticket(
        _ticket(),
        ai_client=_StaticClient(
            _output(
                "\n".join(
                    [
                        "1. Verify: Confirm workspace ACME-001 is affected and the dashboard fails after refresh.",
                        "2. Inspect: Check browser console, network errors, backend logs, and similar solved tickets.",
                        "3. Try: Apply the matching workaround from similar solved tickets.",
                        "4. Confirm: Determine if the issue is better after review.",
                        "5. Close: Save the workaround; create a defect only if the issue remains reproducible.",
                    ]
                )
            )
        ),
    )

    assert "determine if" not in output.recommended_action.lower()
    assert not triage_quality_findings(output)


class _StaticClient:
    def __init__(self, response: dict) -> None:
        self.response = response

    def analyze(self, prompt: str, ticket: Ticket) -> dict:
        return self.response


class _RepairingClient:
    def __init__(self) -> None:
        self.call_count = 0
        self.second_prompt = ""

    def analyze(self, prompt: str, ticket: Ticket) -> dict:
        self.call_count += 1
        if self.call_count == 1:
            return _output(
                "1. Verify: Check the workspace.\n2. Inspect: Escalate to engineering for logs.",
                "We will investigate and update you shortly.",
            )
        self.second_prompt = prompt
        return _output(
            _good_action(),
            "We will verify workspace ACME-001, inspect dashboard errors, and try a cache/session refresh workaround before asking for extra browser details.",
        )
