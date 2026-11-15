def test_logistics_route_recommendation(client, auth_headers):
    """Test logistics route recommendation for intra-state cargo."""
    payload = {
        "origin_pincode": "570001",  # Mysuru
        "destination_pincode": "560001",  # Bengaluru
        "weight_kg": 85.0,
        "target_delivery_date": "2026-11-28"
    }
    response = client.post("/api/v1/ai/logistics/recommend-route", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["recommended_carriers"]) >= 1
    top_carrier = data["recommended_carriers"][0]
    assert "carrier_name" in top_carrier
    assert top_carrier["estimated_cost"] > 0
    assert top_carrier["estimated_transit_hours"] > 0
    assert "KSRTC" in top_carrier["carrier_name"] or "Cargo" in top_carrier["carrier_name"]


def test_logistics_alias_support(client, auth_headers):
    """Test that 'origin' and 'destination' aliases from existing backend client work seamlessly."""
    payload = {
        "origin": "570001",
        "destination": "560001",
        "weight_kg": 25.0
    }
    response = client.post("/api/v1/ai/logistics/recommend-route", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_logistics_invalid_pincode(client, auth_headers):
    """Test that invalid PIN codes (letters or wrong length) are rejected with HTTP 400."""
    payload = {
        "origin_pincode": "ABC1234",
        "destination_pincode": "560001",
        "weight_kg": 10.0
    }
    response = client.post("/api/v1/ai/logistics/recommend-route", json=payload, headers=auth_headers)
    assert response.status_code == 400
    err = response.json()
    assert err["success"] is False

