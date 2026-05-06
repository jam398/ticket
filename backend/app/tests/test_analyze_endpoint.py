def _ticket_payload(title: str = "Duplicate billing charge") -> dict:
    return {
        "title": title,
        "description": "The customer was charged twice for the monthly subscription.",
        "customer_name": "Priya Shah",
        "customer_email": "priya@example.com",
        "source": "email",
        "tags": ["billing"],
    }


def test_analyze_endpoint_saves_analysis_and_does_not_overwrite_ticket_fields(client):
    create_response = client.post("/api/tickets", json=_ticket_payload())
    assert create_response.status_code == 201
    created = create_response.json()

    response = client.post(f"/api/tickets/{created['id']}/analyze")

    assert response.status_code == 200
    detail = response.json()
    assert detail["ticket"]["category"] == "general_question"
    assert detail["ticket"]["priority"] == "medium"
    assert detail["ticket"]["assigned_team"] == "support"
    assert detail["latest_analysis"]["category"] == "billing"
    assert detail["latest_analysis"]["priority"] == "high"
    assert detail["latest_analysis"]["assigned_team"] == "billing"
    assert detail["latest_analysis"]["confidence_label"] == "High"
    combined_guidance = (
        detail["latest_analysis"]["suggested_response"] + " " + detail["latest_analysis"]["recommended_action"]
    ).lower()
    assert "route to" not in combined_guidance
    assert "right team" not in combined_guidance
    assert "verify" in combined_guidance
    action_lines = detail["latest_analysis"]["recommended_action"].splitlines()
    assert len(action_lines) == 5
    assert action_lines[0].startswith("1. Verify:")
    assert action_lines[1].startswith("2. Inspect:")
    assert action_lines[2].startswith("3. Try:")
    assert action_lines[3].startswith("4. Confirm:")
    assert action_lines[4].startswith("5. Close:")
    assert detail["latest_analysis"]["warnings"] == [
        "No similar past tickets were found. Analysis is based only on the current ticket."
    ]
    assert "ai_triage_generated" in [event["event_type"] for event in detail["events"]]


def test_apply_analysis_requires_explicit_call_and_creates_event(client):
    create_response = client.post("/api/tickets", json=_ticket_payload())
    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]

    analyzed = client.post(f"/api/tickets/{ticket_id}/analyze").json()
    analysis_id = analyzed["latest_analysis"]["id"]

    response = client.post(f"/api/tickets/{ticket_id}/apply-analysis/{analysis_id}")

    assert response.status_code == 200
    detail = response.json()
    assert detail["ticket"]["category"] == "billing"
    assert detail["ticket"]["priority"] == "high"
    assert detail["ticket"]["assigned_team"] == "billing"
    event_types = [event["event_type"] for event in detail["events"]]
    assert "ai_suggestion_applied" in event_types


def test_apply_analysis_allows_human_reviewed_overrides(client):
    create_response = client.post("/api/tickets", json=_ticket_payload())
    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]

    analyzed = client.post(f"/api/tickets/{ticket_id}/analyze").json()
    analysis_id = analyzed["latest_analysis"]["id"]

    response = client.post(
        f"/api/tickets/{ticket_id}/apply-analysis/{analysis_id}",
        json={"category": "technical_issue", "priority": "urgent", "assigned_team": "engineering"},
    )

    assert response.status_code == 200
    detail = response.json()
    assert detail["ticket"]["category"] == "technical_issue"
    assert detail["ticket"]["priority"] == "urgent"
    assert detail["ticket"]["assigned_team"] == "engineering"


def test_apply_analysis_rejects_missing_analysis(client):
    create_response = client.post("/api/tickets", json=_ticket_payload())
    assert create_response.status_code == 201

    response = client.post(f"/api/tickets/{create_response.json()['id']}/apply-analysis/999")

    assert response.status_code == 404
