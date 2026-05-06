from app.services.seed_data import seed_database


def test_dashboard_stats_returns_required_counts(client, session):
    seed_database(session)

    response = client.get("/api/dashboard/stats")

    assert response.status_code == 200
    stats = response.json()
    assert stats["total_tickets"] == 100
    assert stats["open"] == 25
    assert stats["in_review"] == 20
    assert stats["waiting_for_customer"] == 15
    assert stats["resolved"] == 25
    assert stats["closed"] == 15
    assert stats["urgent"] == 10
    assert stats["high"] == 28
    assert "overdue" in stats
    assert stats["average_confidence_score"] == 0.0
