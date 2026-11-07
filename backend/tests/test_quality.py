from tests.conftest import get_auth_header
from app.models.work import ProductionBatch, BatchStatus, WorkAllocation
from app.models.quality import QualityInspection, QualityStatus
from app.models.order import BulkOrder, OrderItem


def test_quality_inspection_ai_and_mandatory_human_review(client, leader_user, sample_product, db_session):
    headers_leader = get_auth_header(leader_user)

    # Setup batch and initial inspection
    order = BulkOrder(order_number="ORD-Q-01", buyer_id=1, shg_id=1, title="Quality Batch Order")
    db_session.add(order)
    db_session.flush()

    item = OrderItem(bulk_order_id=order.id, product_id=sample_product.id, quantity=30)
    db_session.add(item)
    db_session.flush()

    alloc = WorkAllocation(bulk_order_id=order.id, order_item_id=item.id, member_id=1, allocated_quantity=30)
    db_session.add(alloc)
    db_session.flush()

    batch = ProductionBatch(
        bulk_order_id=order.id,
        work_allocation_id=alloc.id,
        batch_number="BATCH-TEST-001",
        quantity=30,
        status=BatchStatus.SUBMITTED.value,
        photo_urls='["/uploads/test.jpg"]'
    )
    db_session.add(batch)
    db_session.flush()

    inspection = QualityInspection(
        production_batch_id=batch.id,
        status=QualityStatus.PENDING_INSPECTION.value
    )
    db_session.add(inspection)
    db_session.commit()

    # 1. Trigger AI inspection -> Sets PENDING_HUMAN_REVIEW (AI cannot make final decision)
    ai_res = client.post(f"/api/v1/quality/inspect/{inspection.id}/ai", headers=headers_leader)
    assert ai_res.status_code == 200
    ai_data = ai_res.json()["data"]
    assert ai_data["status"] == "PENDING_HUMAN_REVIEW"
    assert ai_data["ai_score"] is not None

    # 2. Rejection without reason must fail (400)
    fail_res = client.put(f"/api/v1/quality/inspect/{inspection.id}/decision", json={
        "human_decision": "REJECTED",
        "rejection_reason": None
    }, headers=headers_leader)
    assert fail_res.status_code == 400

    # 3. Human reviewer records approval
    ok_res = client.put(f"/api/v1/quality/inspect/{inspection.id}/decision", json={
        "human_decision": "APPROVED",
        "rejection_reason": None
    }, headers=headers_leader)
    assert ok_res.status_code == 200
    assert ok_res.json()["data"]["status"] == "APPROVED"
    assert ok_res.json()["data"]["human_decision"] == "APPROVED"

    # Batch status should now be ACCEPTED
    db_session.refresh(batch)
    assert batch.status == BatchStatus.ACCEPTED.value
