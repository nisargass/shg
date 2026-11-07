from tests.conftest import get_auth_header
from app.models.order import OrderStatus


def test_create_bulk_order(client, buyer_user, sample_product):
    headers = get_auth_header(buyer_user)
    payload = {
        "title": "500 Artisan Tote Bags",
        "description": "Standard stitched bag for corporate event",
        "target_delivery_date": "2026-12-01T00:00:00Z",
        "currency": "INR",
        "items": [
            {
                "product_id": sample_product.id,
                "quantity": 500,
                "unit_price": 150.0,
                "specifications": "Reinforced strap"
            }
        ]
    }
    res = client.post("/api/v1/orders", json=payload, headers=headers)
    assert res.status_code == 201
    data = res.json()["data"]
    assert data["status"] == "DRAFT"
    assert data["total_order_value"] == 75000.0
    assert len(data["items"]) == 1


def test_order_status_lifecycle_transitions(client, buyer_user, leader_user, sample_product):
    headers_buyer = get_auth_header(buyer_user)
    headers_leader = get_auth_header(leader_user)

    # 1. Create Order in DRAFT
    payload = {
        "title": "Sample Order",
        "items": [{"product_id": sample_product.id, "quantity": 100, "unit_price": 100.0}]
    }
    res = client.post("/api/v1/orders", json=payload, headers=headers_buyer)
    order_id = res.json()["data"]["id"]

    # 2. Transition: DRAFT -> SUBMITTED (Valid)
    res = client.post(f"/api/v1/orders/{order_id}/transition", json={"new_status": "SUBMITTED"}, headers=headers_buyer)
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "SUBMITTED"

    # 3. Transition: SUBMITTED -> ACCEPTED (Valid)
    res = client.post(f"/api/v1/orders/{order_id}/transition", json={"new_status": "ACCEPTED"}, headers=headers_leader)
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "ACCEPTED"

    # 4. Invalid Transition: ACCEPTED -> COMPLETED (Must fail 400 Bad Request)
    res = client.post(f"/api/v1/orders/{order_id}/transition", json={"new_status": "COMPLETED"}, headers=headers_leader)
    assert res.status_code == 400
    assert "Invalid order status transition" in res.json()["detail"]
