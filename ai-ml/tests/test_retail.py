def test_retail_demand_forecast_sufficient_data(client, auth_headers):
    """Test retail demand forecasting with historical trend and festive surge."""
    payload = {
        "product_id": 3,
        "historical_sales": [
            {"month": "2026-06", "quantity": 100},
            {"month": "2026-07", "quantity": 120},
            {"month": "2026-08", "quantity": 150},
            {"month": "2026-09", "quantity": 190}
        ],
        "upcoming_festival_season": True
    }
    response = client.post("/api/v1/ai/retail/forecast-demand", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["product_id"] == 3
    assert data["forecasted_monthly_demand"] > 190  # Positive trend + festive surge
    assert len(data["confidence_interval"]) == 2
    assert data["confidence_interval"][0] <= data["forecasted_monthly_demand"] <= data["confidence_interval"][1]
    assert data["confidence_score"] >= 0.80
    assert "festiv" in str(data["seasonal_factor"]).lower()


def test_retail_demand_insufficient_data_handling(client, auth_headers):
    """Test that insufficient historical data honestly reports low confidence."""
    payload = {
        "product_id": 3,
        "historical_sales": [
            {"month": "2026-10", "quantity": 50}
        ],
        "upcoming_festival_season": False
    }
    response = client.post("/api/v1/ai/retail/forecast-demand", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["confidence_score"] <= 0.50
    assert "insufficient" in data["explanation"].lower()

