def test_worker_completion_likelihood_success(client, auth_headers):
    """Test worker likelihood calculation with realistic capacity and factors."""
    payload = {
        "member_id": 14,
        "product_id": 3,
        "proposed_quantity": 40,
        "deadline": "2026-11-20T18:00:00Z",
        "available_hours_per_day": 6.0,
        "current_workload": 5.0,
        "historical_completion_rate": 96.5,
        "skills": ["stitching", "embroidery"]
    }
    response = client.post("/api/v1/ai/workforce/completion-likelihood", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["member_id"] == 14
    assert 0.0 <= data["completion_likelihood_percentage"] <= 100.0
    assert "estimated_completion_date" in data
    assert "factors" in data
    assert len(data["factors"]) > 0
    assert "explanation" in data


def test_worker_likelihood_past_deadline_risk(client, auth_headers):
    """Test that a tight or past deadline reduces completion likelihood."""
    payload = {
        "member_id": 14,
        "product_id": 3,
        "proposed_quantity": 200,  # Huge batch
        "deadline": "2026-11-09T00:00:00Z",  # Imminent deadline
        "available_hours_per_day": 2.0,  # Low hours
        "current_workload": 50.0,
        "historical_completion_rate": 70.0,
        "skills": []
    }
    response = client.post("/api/v1/ai/workforce/completion-likelihood", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["completion_likelihood_percentage"] < 70.0  # Must reflect severe risk

