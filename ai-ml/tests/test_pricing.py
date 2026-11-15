def test_pricing_calculation_exact_formulas(client, auth_headers):
    """Test exact mathematical formulas for pricing recommendation."""
    # Total cost = 45000 + 25000 + 3000 + 4000 + 2000 = 79000
    # Qty = 500 -> Unit cost = 79000 / 500 = 158.00
    # Margin = 15% -> SP = 158 / (1 - 0.15) = 158 / 0.85 = 185.88
    # Total Value = 185.88 * 500 = 92940.0
    payload = {
        "bulk_order_id": 22,
        "material_cost": 45000.0,
        "labor_cost": 25000.0,
        "packaging_cost": 3000.0,
        "transport_cost": 4000.0,
        "operational_expenses": 2000.0,
        "quantity": 500,
        "target_margin_percentage": 15.0
    }
    response = client.post("/api/v1/ai/pricing/recommend", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["recommended_selling_price_per_unit"] == 185.88
    assert data["recommended_total_order_value"] == 92940.0
    assert data["estimated_profit"] == 13940.0  # 92940 - 79000
    assert abs(data["margin_percentage"] - 15.0) < 0.1


def test_pricing_missing_cost_warnings(client, auth_headers):
    """Test that zero operational or transport costs trigger warnings."""
    payload = {
        "bulk_order_id": 23,
        "material_cost": 10000.0,
        "labor_cost": 5000.0,
        "packaging_cost": 0.0,  # Zero packaging
        "transport_cost": 0.0,  # Zero transport
        "operational_expenses": 0.0,  # Zero operational
        "quantity": 100,
        "target_margin_percentage": 20.0
    }
    response = client.post("/api/v1/ai/pricing/recommend", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["missing_cost_warnings"]) >= 3


def test_pricing_invalid_margin_validation(client, auth_headers):
    """Test that margin >= 100% is rejected by validation."""
    payload = {
        "bulk_order_id": 24,
        "material_cost": 1000.0,
        "labor_cost": 500.0,
        "packaging_cost": 100.0,
        "transport_cost": 50.0,
        "operational_expenses": 50.0,
        "quantity": 10,
        "target_margin_percentage": 100.0  # Impossible division by zero margin
    }
    response = client.post("/api/v1/ai/pricing/recommend", json=payload, headers=auth_headers)
    assert response.status_code == 422

