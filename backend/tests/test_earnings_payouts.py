from tests.conftest import get_auth_header
from app.models.user import SHGMember, User
from app.models.work import WorkAllocation, AllocationStatus
from app.models.order import BulkOrder, OrderItem
from app.models.finance import MemberEarning, Payout, PayoutStatus, EarningPaymentStatus
from app.core.security import hash_password


def test_earnings_and_strict_member_financial_privacy(client, leader_user, member_user, sample_product, db_session):
    headers_leader = get_auth_header(leader_user)
    headers_member1 = get_auth_header(member_user)

    # Create a second member for privacy test
    user2 = User(
        email="member2@shg.org",
        hashed_password=hash_password("password123"),
        full_name="Geetha Member",
        role="SHG_MEMBER",
        is_active=True
    )
    db_session.add(user2)
    db_session.flush()

    member2 = SHGMember(user_id=user2.id, shg_id=1, is_active=True)
    db_session.add(member2)
    db_session.flush()

    member1 = db_session.query(SHGMember).filter(SHGMember.user_id == member_user.id).first()

    # Create order & allocations
    order = BulkOrder(order_number="ORD-FIN-01", buyer_id=1, shg_id=1, title="Finance Test Order")
    db_session.add(order)
    db_session.flush()

    item = OrderItem(bulk_order_id=order.id, product_id=sample_product.id, quantity=100)
    db_session.add(item)
    db_session.flush()

    alloc1 = WorkAllocation(
        bulk_order_id=order.id,
        order_item_id=item.id,
        member_id=member1.id,
        allocated_quantity=50,
        completed_quantity=50,
        unit_rate=50.0,
        status=AllocationStatus.COMPLETED.value
    )
    alloc2 = WorkAllocation(
        bulk_order_id=order.id,
        order_item_id=item.id,
        member_id=member2.id,
        allocated_quantity=50,
        completed_quantity=50,
        unit_rate=50.0,
        status=AllocationStatus.COMPLETED.value
    )
    db_session.add_all([alloc1, alloc2])
    db_session.commit()

    # 1. Leader calculates earnings for Member 1: 50 units * 50 = 2500 gross, 100 deduction = 2400 net
    calc_res1 = client.post(f"/api/v1/earnings/calculate/{alloc1.id}?deductions=100.0&deductions_reason=Thread%20shortage", headers=headers_leader)
    assert calc_res1.status_code == 200
    e1_data = calc_res1.json()["data"]
    assert e1_data["gross_earnings"] == 2500.0
    assert e1_data["deductions"] == 100.0
    assert e1_data["net_payable_amount"] == 2400.0

    # Calculate earnings for Member 2
    calc_res2 = client.post(f"/api/v1/earnings/calculate/{alloc2.id}", headers=headers_leader)
    assert calc_res2.status_code == 200

    # 2. Strict Privacy Test: Member 1 calls /api/v1/earnings/me -> Must see ONLY Member 1's earnings!
    my_earnings_res = client.get("/api/v1/earnings/me", headers=headers_member1)
    assert my_earnings_res.status_code == 200
    my_list = my_earnings_res.json()["data"]
    assert len(my_list) == 1
    assert my_list[0]["member_id"] == member1.id
    assert my_list[0]["net_payable_amount"] == 2400.0


def test_group_payout_approval_and_genuine_payment(client, leader_user, member_user, sample_product, db_session):
    headers_leader = get_auth_header(leader_user)
    member = db_session.query(SHGMember).filter(SHGMember.user_id == member_user.id).first()

    # Create calculated earning ready for payout
    earning = MemberEarning(
        member_id=member.id,
        bulk_order_id=1,
        work_allocation_id=1,
        assigned_quantity=40,
        accepted_quantity=40,
        approved_rate=50.0,
        gross_earnings=2000.0,
        deductions=0.0,
        net_payable_amount=2000.0,
        payment_status=EarningPaymentStatus.CALCULATED.value
    )
    db_session.add(earning)
    db_session.commit()

    # 1. Create consolidated payout batch
    payout_res = client.post("/api/v1/payouts", json={
        "shg_id": 1,
        "notes": "November Artisan Payout Cycle"
    }, headers=headers_leader)
    assert payout_res.status_code == 201
    payout_id = payout_res.json()["data"]["id"]
    assert payout_res.json()["data"]["status"] == PayoutStatus.PENDING_GROUP_APPROVAL.value
    assert payout_res.json()["data"]["total_amount"] == 2000.0

    # 2. Leader approves payout batch -> status moves to PAYMENT_PENDING
    appr_res = client.put(f"/api/v1/payouts/{payout_id}/approval", json={
        "decision": "APPROVED",
        "notes": "Reviewed and agreed by group committee"
    }, headers=headers_leader)
    assert appr_res.status_code == 200
    assert appr_res.json()["data"]["status"] == PayoutStatus.PAYMENT_PENDING.value

    # 3. Confirm Genuine Bank Payment (requires authentic transaction reference)
    pay_res = client.put(f"/api/v1/payouts/{payout_id}/confirm-payment", json={
        "payment_method": "Bank Transfer (NEFT)",
        "transaction_ref": "NEFT-SBI-20261107-994411",
        "payment_date": "2026-11-07T12:00:00Z",
        "notes": "Transaction confirmed via Bank Statement"
    }, headers=headers_leader)
    assert pay_res.status_code == 200
    assert pay_res.json()["data"]["status"] == PayoutStatus.PAID.value
    assert pay_res.json()["data"]["transaction_ref"] == "NEFT-SBI-20261107-994411"

    # Member earning status must now be PAID
    db_session.refresh(earning)
    assert earning.payment_status == EarningPaymentStatus.PAID.value
