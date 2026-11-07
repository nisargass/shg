from tests.conftest import get_auth_header


def test_pricing_calculation_and_leader_approval(client, leader_user, buyer_user, sample_product):
    headers_buyer = get_auth_header(buyer_user)
    headers_leader = get_auth_header(leader_user)

    # Create Order with 100 units
    order_res = client.post("/api/v1/orders", json={
        "title": "Pricing Test Order",
        "items": [{"product_id": sample_product.id, "quantity": 100, "unit_price": 0.0}]
    }, headers=headers_buyer)
    order_id = order_res.json()["data"]["id"]

    # Calculate pricing
    # Material: 5000, Labor: 3000, Packaging: 500, Transport: 1000, Ops: 500 = Total Cost 10000
    # Cost per unit = 10000 / 100 = 100
    # Margin 20% -> Suggested Selling Price = 120
    pricing_payload = {
        "bulk_order_id": order_id,
        "total_material_cost": 5000.0,
        "labor_cost": 3000.0,
        "packaging_cost": 500.0,
        "transportation_cost": 1000.0,
        "operational_expenses": 500.0,
        "profit_margin_percentage": 20.0,
        "notes": "Costing test breakdown"
    }
    p_res = client.post("/api/v1/pricing", json=pricing_payload, headers=headers_leader)
    assert p_res.status_code == 201
    p_data = p_res.json()["data"]
    assert p_data["total_cost"] == 10000.0
    assert p_data["calculated_unit_price"] == 100.0
    assert p_data["suggested_selling_price"] == 120.0
    assert p_data["is_approved"] is False

    # Leader approves pricing
    pricing_id = p_data["id"]
    approval_res = client.put(f"/api/v1/pricing/{pricing_id}/approve", json={
        "is_approved": True,
        "final_approved_price": 125.0,
        "notes": "Approved with rounding"
    }, headers=headers_leader)
    assert approval_res.status_code == 200
    assert approval_res.json()["data"]["is_approved"] is True
    assert approval_res.json()["data"]["final_approved_price"] == 125.0
