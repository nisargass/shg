def test_inventory_forecast_stockout_high_urgency(client, auth_headers):
    """Test stockout calculation and high restocking urgency."""
    payload = {
        "shg_id": 1,
        "inventory_id": 8,
        "current_physical_stock": 25.0,
        "bulk_committed_stock": 20.0,  # Only 5.0 usable stock left!
        "lead_time_days": 7,
        "daily_burn_rate": 3.5  # 5.0 / 3.5 = 1.4 days until stockout
    }
    response = client.post("/api/v1/ai/inventory/forecast-restock", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["inventory_id"] == 8
    assert data["days_until_stockout"] == 1.4
    assert data["restock_recommended"] is True
    assert data["urgency"] in ["CRITICAL", "HIGH"]
    assert data["recommended_order_quantity"] > 0


def test_inventory_forecast_healthy_stock(client, auth_headers):
    """Test inventory with ample stock shows LOW urgency."""
    payload = {
        "shg_id": 1,
        "inventory_id": 9,
        "current_physical_stock": 200.0,
        "bulk_committed_stock": 20.0,  # 180 usable
        "lead_time_days": 5,
        "daily_burn_rate": 2.0  # 90 days of stock
    }
    response = client.post("/api/v1/ai/inventory/forecast-restock", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["days_until_stockout"] >= 80.0
    assert data["restock_recommended"] is False
    assert data["urgency"] == "LOW"

