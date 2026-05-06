from datetime import datetime, timedelta

from app.models import utc_now


def _ticket_payload() -> dict:
    return {
        "title": "Dashboard export not received",
        "description": "The customer requested an export but the email never arrived.",
        "customer_name": "Jamie Chen",
        "customer_email": "jamie@example.com",
        "source": "email",
        "tags": ["export", "reporting"],
    }


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def test_create_ticket_records_creation_event(client):
    response = client.post("/api/tickets", json=_ticket_payload())

    assert response.status_code == 201
    ticket = response.json()

    detail_response = client.get(f"/api/tickets/{ticket['id']}")
    assert detail_response.status_code == 200
    events = detail_response.json()["events"]

    assert len(events) == 1
    assert events[0]["ticket_id"] == ticket["id"]
    assert events[0]["event_type"] == "ticket_created"
    assert events[0]["message"] == "Ticket created."
    assert events[0]["created_at"] is not None


def test_important_ticket_updates_record_clear_events_and_recalculate_due_at(client):
    create_response = client.post("/api/tickets", json=_ticket_payload())
    assert create_response.status_code == 201
    created = create_response.json()
    original_due_at = _parse_datetime(created["due_at"])

    before_update = utc_now()
    update_response = client.patch(
        f"/api/tickets/{created['id']}",
        json={"status": "in_review", "priority": "urgent", "assigned_team": "engineering"},
    )
    after_update = utc_now()

    assert update_response.status_code == 200
    updated = update_response.json()
    recalculated_due_at = _parse_datetime(updated["due_at"])
    assert recalculated_due_at < original_due_at
    assert before_update + timedelta(hours=1) <= recalculated_due_at <= after_update + timedelta(
        hours=1,
        seconds=1,
    )

    detail = client.get(f"/api/tickets/{created['id']}").json()
    messages_by_type = {event["event_type"]: event["message"] for event in detail["events"]}

    assert messages_by_type["status_changed"] == "Status changed from Open to In Review."
    assert messages_by_type["priority_changed"] == "Priority changed from Medium to Urgent."
    assert (
        messages_by_type["assigned_team_changed"]
        == "Assigned team changed from Support to Engineering."
    )


def test_noop_ticket_update_does_not_add_change_events(client):
    create_response = client.post("/api/tickets", json=_ticket_payload())
    assert create_response.status_code == 201
    created = create_response.json()

    update_response = client.patch(
        f"/api/tickets/{created['id']}",
        json={"status": "open", "priority": "medium", "assigned_team": "support"},
    )

    assert update_response.status_code == 200
    detail = client.get(f"/api/tickets/{created['id']}").json()
    assert [event["event_type"] for event in detail["events"]] == ["ticket_created"]


def test_ai_analysis_and_apply_create_events(client):
    create_response = client.post("/api/tickets", json=_ticket_payload())
    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]

    analyzed = client.post(f"/api/tickets/{ticket_id}/analyze").json()
    analysis_id = analyzed["latest_analysis"]["id"]
    applied = client.post(f"/api/tickets/{ticket_id}/apply-analysis/{analysis_id}").json()

    event_types = [event["event_type"] for event in applied["events"]]
    assert "ai_triage_generated" in event_types
    assert "ai_suggestion_applied" in event_types


def test_resolve_creates_resolution_events(client):
    create_response = client.post("/api/tickets", json=_ticket_payload())
    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]

    resolved = client.patch(
        f"/api/tickets/{ticket_id}/resolve",
        json={"resolution_notes": "Reset access and confirmed the customer could sign in."},
    ).json()
    updated = client.patch(
        f"/api/tickets/{ticket_id}/resolve",
        json={"resolution_notes": "Updated resolution after customer confirmation."},
    ).json()

    assert "ticket_resolved" in [event["event_type"] for event in resolved["events"]]
    assert "resolution_updated" in [event["event_type"] for event in updated["events"]]
