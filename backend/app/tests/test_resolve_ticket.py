def _ticket_payload(title: str = "Payment method declined") -> dict:
    return {
        "title": title,
        "description": "Customer cannot complete payment because the payment method is declined.",
        "customer_name": "Resolve Customer",
        "customer_email": "resolve@example.com",
        "source": "email",
        "tags": ["billing"],
    }


def test_resolve_rejects_empty_resolution_notes(client):
    created = client.post("/api/tickets", json=_ticket_payload()).json()

    response = client.patch(f"/api/tickets/{created['id']}/resolve", json={"resolution_notes": " "})

    assert response.status_code == 422


def test_resolve_sets_status_notes_timestamp_event_and_vector_context(client):
    created = client.post("/api/tickets", json=_ticket_payload()).json()
    notes = "Confirmed card decline, sent secure payment update link, and verified payment succeeded."

    response = client.patch(f"/api/tickets/{created['id']}/resolve", json={"resolution_notes": notes})

    assert response.status_code == 200
    detail = response.json()
    assert detail["ticket"]["status"] == "resolved"
    assert detail["ticket"]["resolved_at"] is not None
    assert detail["ticket"]["resolution_notes"] == notes
    assert "ticket_resolved" in [event["event_type"] for event in detail["events"]]

    similar = client.post(
        "/api/tickets",
        json=_ticket_payload("Payment method declined again"),
    ).json()
    analyzed = client.post(f"/api/tickets/{similar['id']}/analyze").json()

    assert analyzed["similar_ticket_matches"]
    assert analyzed["similar_ticket_matches"][0]["matched_ticket"]["resolution_notes"] == notes


def test_resolve_existing_resolved_ticket_updates_notes_and_event(client):
    created = client.post("/api/tickets", json=_ticket_payload()).json()
    first = "Initial resolution notes."
    second = "Updated resolution notes after customer confirmed payment."

    assert client.patch(f"/api/tickets/{created['id']}/resolve", json={"resolution_notes": first}).status_code == 200
    response = client.patch(f"/api/tickets/{created['id']}/resolve", json={"resolution_notes": second})

    assert response.status_code == 200
    detail = response.json()
    assert detail["ticket"]["resolution_notes"] == second
    assert "resolution_updated" in [event["event_type"] for event in detail["events"]]
