from tests.conftest import get_auth_header
from app.models.user import SHGMember


def test_work_allocation_limit_validation(client, leader_user, member_user, buyer_user, sample_product, db_session):
    headers_buyer = get_auth_header(buyer_user)
    headers_leader = get_auth_header(leader_user)

    # Create Order for 50 units
    order_res = client.post("/api/v1/orders", json={
        "title": "Allocation Test Order",
        "items": [{"product_id": sample_product.id, "quantity": 50, "unit_price": 100.0}]
    }, headers=headers_buyer)
    order_data = order_res.json()["data"]
    order_id = order_data["id"]
    order_item_id = order_data["items"][0]["id"]

    member = db_session.query(SHGMember).filter(SHGMember.user_id == member_user.id).first()

    # Attempt to allocate 60 units (exceeds order item quantity of 50) -> Must fail
    exceed_payload = {
        "bulk_order_id": order_id,
        "order_item_id": order_item_id,
        "allocations": [
            {
                "bulk_order_id": order_id,
                "order_item_id": order_item_id,
                "member_id": member.id,
                "allocated_quantity": 60,
                "unit_rate": 40.0
            }
        ]
    }
    fail_res = client.post("/api/v1/allocations/propose", json=exceed_payload, headers=headers_leader)
    assert fail_res.status_code == 400
    assert "exceeds item quantity" in fail_res.json()["detail"]

    # Valid allocation of 40 units -> Succeeds in PROPOSED state
    valid_payload = {
        "bulk_order_id": order_id,
        "order_item_id": order_item_id,
        "allocations": [
            {
                "bulk_order_id": order_id,
                "order_item_id": order_item_id,
                "member_id": member.id,
                "allocated_quantity": 40,
                "unit_rate": 40.0
            }
        ]
    }
    ok_res = client.post("/api/v1/allocations/propose", json=valid_payload, headers=headers_leader)
    assert ok_res.status_code == 201
    alloc_id = ok_res.json()["data"][0]["id"]
    assert ok_res.json()["data"][0]["status"] == "PROPOSED"

    # Leader approves the allocation
    approve_res = client.put(f"/api/v1/allocations/{alloc_id}", json={
        "status": "APPROVED_BY_LEADER"
    }, headers=headers_leader)
    assert approve_res.status_code == 200
    assert approve_res.json()["data"]["status"] == "APPROVED_BY_LEADER"
