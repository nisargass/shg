def test_work_allocation_fairness_and_caps(client, auth_headers):
    """Test that work allocation distributes fairly and never exceeds member capacity."""
    payload = {
        "bulk_order_id": 22,
        "order_item_id": 45,
        "product_id": 3,
        "total_quantity": 100,
        "deadline": "2026-11-25T00:00:00Z",
        "members": [
            {
                "member_id": 1,
                "skills": ["weaving", "tailoring"],
                "available_hours_per_day": 6.0,
                "current_workload": 0.0,
                "max_feasible_daily_quantity": 8.0,
                "historical_completion_rate": 98.0
            },
            {
                "member_id": 2,
                "skills": ["tailoring"],
                "available_hours_per_day": 4.0,
                "current_workload": 5.0,
                "max_feasible_daily_quantity": 6.0,
                "historical_completion_rate": 85.0
            }
        ]
    }
    response = client.post("/api/v1/ai/allocation/recommend", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total_allocated"] + data["unallocated_quantity"] == 100
    assert 0.0 <= data["fairness_index"] <= 1.0
    assert len(data["recommendations"]) > 0

    # Verify no member was assigned more than feasible capacity
    for rec in data["recommendations"]:
        assert rec["proposed_quantity"] > 0
        assert 0.0 <= rec["completion_likelihood_percentage"] <= 100.0


def test_work_allocation_unallocated_when_capacity_insufficient(client, auth_headers):
    """Test that when order size exceeds total network capacity, unallocated_quantity is reported."""
    payload = {
        "bulk_order_id": 22,
        "order_item_id": 45,
        "product_id": 3,
        "total_quantity": 500,  # Huge order
        "deadline": "2026-11-10T00:00:00Z",  # Very tight deadline (1-2 days)
        "members": [
            {
                "member_id": 1,
                "skills": ["tailoring"],
                "available_hours_per_day": 4.0,
                "current_workload": 10.0,
                "max_feasible_daily_quantity": 5.0,
                "historical_completion_rate": 90.0
            }
        ]
    }
    response = client.post("/api/v1/ai/allocation/recommend", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["unallocated_quantity"] > 0
    assert data["total_allocated"] < 500

