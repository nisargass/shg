def test_protected_endpoint_missing_key(client):
    """Test that missing X-SHG-Service-Key is rejected with HTTP 401."""
    payload = {
        "bulk_order_id": 1,
        "material_cost": 1000.0,
        "labor_cost": 500.0,
        "packaging_cost": 100.0,
        "transport_cost": 50.0,
        "operational_expenses": 50.0,
        "quantity": 10,
        "target_margin_percentage": 15.0
    }
    # No headers provided
    response = client.post("/api/v1/ai/pricing/recommend", json=payload)
    assert response.status_code == 401
    err = response.json()
    assert err["success"] is False
    assert err["error"]["code"] == "AUTHENTICATION_FAILED"


def test_protected_endpoint_invalid_key(client, invalid_auth_headers):
    """Test that incorrect X-SHG-Service-Key is rejected with HTTP 403."""
    payload = {
        "bulk_order_id": 1,
        "material_cost": 1000.0,
        "labor_cost": 500.0,
        "packaging_cost": 100.0,
        "transport_cost": 50.0,
        "operational_expenses": 50.0,
        "quantity": 10,
        "target_margin_percentage": 15.0
    }
    response = client.post("/api/v1/ai/pricing/recommend", json=payload, headers=invalid_auth_headers)
    assert response.status_code == 403
    err = response.json()
    assert err["success"] is False
    assert err["error"]["code"] == "AUTHENTICATION_FAILED"


def test_protected_endpoint_valid_key(client, auth_headers):
    """Test that valid X-SHG-Service-Key passes authentication."""
    payload = {
        "bulk_order_id": 1,
        "material_cost": 1000.0,
        "labor_cost": 500.0,
        "packaging_cost": 100.0,
        "transport_cost": 50.0,
        "operational_expenses": 50.0,
        "quantity": 10,
        "target_margin_percentage": 15.0
    }
    response = client.post("/api/v1/ai/pricing/recommend", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

