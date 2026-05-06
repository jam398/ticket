def _create_ticket(client, title: str, source: str = "email") -> int:
    response = client.post(
        "/api/tickets",
        json={
            "title": title,
            "description": f"{title} needs support follow-up.",
            "customer_name": "Test Customer",
            "customer_email": f"{title.replace(' ', '.').lower()}@example.com",
            "source": source,
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_ticket_filters_cover_required_fields(client):
    billing_id = _create_ticket(client, "Duplicate charge", "email")
    bug_id = _create_ticket(client, "Export file missing rows", "chat")

    client.patch(
        f"/api/tickets/{billing_id}",
        json={"category": "billing", "priority": "high", "assigned_team": "billing"},
    )
    client.patch(
        f"/api/tickets/{bug_id}",
        json={
            "status": "waiting_for_customer",
            "category": "bug_report",
            "priority": "urgent",
            "assigned_team": "engineering",
        },
    )

    assert client.get("/api/tickets?status=waiting_for_customer").json()["total"] == 1
    assert client.get("/api/tickets?category=billing").json()["items"][0]["id"] == billing_id
    assert client.get("/api/tickets?priority=urgent").json()["items"][0]["id"] == bug_id
    assert client.get("/api/tickets?assigned_team=engineering").json()["items"][0]["id"] == bug_id
    assert client.get("/api/tickets?source=chat").json()["items"][0]["id"] == bug_id
    assert client.get("/api/tickets?search=duplicate").json()["items"][0]["id"] == billing_id
