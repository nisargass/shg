from tests.conftest import get_auth_header
from app.models.user import SHGMember
from app.models.work import WorkAllocation, AllocationStatus


def test_production_progress_and_verified_calculation(client, leader_user, member_user, buyer_user, sample_product, db_session):
    headers_member = get_auth_header(member_user)

    # Setup approved allocation directly for testing
    member = db_session.query(SHGMember).filter(SHGMember.user_id == member_user.id).first()
    
    # Create order directly
    from app.models.order import BulkOrder, OrderItem
    order = BulkOrder(
        order_number="ORD-TEST-001",
        buyer_id=1,
        shg_id=1,
        title="Production Bag Order",
        status="IN_PRODUCTION"
    )
    db_session.add(order)
    db_session.flush()

    item = OrderItem(
        bulk_order_id=order.id,
        product_id=sample_product.id,
        quantity=50,
        pending_quantity=50,
        completed_quantity=0
    )
    db_session.add(item)
    db_session.flush()

    alloc = WorkAllocation(
        bulk_order_id=order.id,
        order_item_id=item.id,
        member_id=member.id,
        allocated_quantity=50,
        completed_quantity=0,
        unit_rate=40.0,
        status=AllocationStatus.APPROVED_BY_LEADER.value
    )
    db_session.add(alloc)
    db_session.commit()

    # Member logs 20 completed units
    res = client.post("/api/v1/production/progress", json={
        "work_allocation_id": alloc.id,
        "quantity_produced": 20,
        "remarks": "Day 1 production complete"
    }, headers=headers_member)
    assert res.status_code == 201

    db_session.refresh(alloc)
    assert alloc.completed_quantity == 20
    # Verified actual progress calculation: 20 / 50 = 40.0%
    assert alloc.progress_percentage == 40.0
    assert alloc.status == AllocationStatus.IN_PROGRESS.value

    # Member submits a completed batch with photos
    batch_res = client.post("/api/v1/production/batch", json={
        "work_allocation_id": alloc.id,
        "quantity": 20,
        "photo_urls": ["/uploads/photo1.jpg"]
    }, headers=headers_member)
    assert batch_res.status_code == 201
    assert batch_res.json()["data"]["quantity"] == 20
    assert batch_res.json()["data"]["status"] == "SUBMITTED"
