def _ticket_payload(title: str = "Password reset email not received") -> dict:
    return {
        "title": title,
        "description": "I requested a password reset email but never received it.",
        "customer_name": "Maria Lopez",
        "customer_email": "maria@example.com",
        "source": "web_form",
        "tags": ["login", "password"],
    }


def test_create_list_get_and_update_ticket(client):
    create_response = client.post("/api/tickets", json=_ticket_payload())

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["status"] == "open"
    assert created["category"] == "general_question"
    assert created["priority"] == "medium"
    assert created["assigned_team"] == "support"
    assert created["due_at"] is not None
    assert created["tags"] == ["login", "password"]

    list_response = client.get("/api/tickets")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    detail_response = client.get(f"/api/tickets/{created['id']}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["ticket"]["id"] == created["id"]
    assert detail["events"][0]["event_type"] == "ticket_created"

    update_response = client.patch(
        f"/api/tickets/{created['id']}",
        json={"status": "in_review", "priority": "high", "assigned_team": "engineering"},
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["status"] == "in_review"
    assert updated["priority"] == "high"
    assert updated["assigned_team"] == "engineering"

    updated_detail = client.get(f"/api/tickets/{created['id']}").json()
    event_types = [event["event_type"] for event in updated_detail["events"]]
    assert "status_changed" in event_types
    assert "priority_changed" in event_types
    assert "assigned_team_changed" in event_types


def test_get_missing_ticket_returns_404(client):
    response = client.get("/api/tickets/999")

    assert response.status_code == 404


def test_empty_title_is_rejected(client):
    payload = _ticket_payload(title=" ")
    response = client.post("/api/tickets", json=payload)

    assert response.status_code == 422
