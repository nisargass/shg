import uuid
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.finance import (
    MemberEarning, Payout, PayoutApproval, GroupApproval,
    EarningPaymentStatus, PayoutStatus, ApprovalDecision
)
from app.models.work import WorkAllocation, AllocationStatus, ProductionBatch, BatchStatus
from app.models.order import BulkOrder
from app.models.user import SHGMember
from app.models.support import Notification
from app.schemas.finance import PayoutCreate, PayoutApprovalRequest, PayoutPaymentConfirmation


class PayoutService:

    @staticmethod
    def calculate_member_earnings_for_allocation(
        db: Session,
        work_allocation_id: int,
        deductions: float = 0.0,
        deductions_reason: Optional[str] = None
    ) -> MemberEarning:
        alloc = db.query(WorkAllocation).filter(WorkAllocation.id == work_allocation_id).first()
        if not alloc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work allocation not found")

        # Sum up only ACCEPTED quantities from verified batches
        accepted_batches = db.query(ProductionBatch).filter(
            ProductionBatch.work_allocation_id == alloc.id,
            ProductionBatch.status == BatchStatus.ACCEPTED.value
        ).all()
        accepted_quantity = sum(b.quantity for b in accepted_batches)

        # Fallback to completed quantity if no individual batch is used but allocation is marked completed
        if accepted_quantity == 0 and alloc.completed_quantity > 0:
            accepted_quantity = alloc.completed_quantity

        rate = alloc.unit_rate
        gross = round(accepted_quantity * rate, 2)
        net = max(0.0, round(gross - deductions, 2))

        earning = db.query(MemberEarning).filter(MemberEarning.work_allocation_id == alloc.id).first()
        if not earning:
            earning = MemberEarning(
                member_id=alloc.member_id,
                bulk_order_id=alloc.bulk_order_id,
                work_allocation_id=alloc.id,
                assigned_quantity=alloc.allocated_quantity,
                accepted_quantity=accepted_quantity,
                approved_rate=rate,
                gross_earnings=gross,
                deductions=deductions,
                deductions_reason=deductions_reason,
                net_payable_amount=net,
                payment_status=EarningPaymentStatus.CALCULATED.value
            )
            db.add(earning)
        else:
            earning.assigned_quantity = alloc.allocated_quantity
            earning.accepted_quantity = accepted_quantity
            earning.approved_rate = rate
            earning.gross_earnings = gross
            earning.deductions = deductions
            earning.deductions_reason = deductions_reason
            earning.net_payable_amount = net

        db.commit()
        db.refresh(earning)
        return earning

    @staticmethod
    def create_group_payout(db: Session, payout_in: PayoutCreate) -> Payout:
        # Sum all calculated earnings in this SHG that are not yet included in a payout
        members = db.query(SHGMember).filter(SHGMember.shg_id == payout_in.shg_id).all()
        member_ids = [m.id for m in members]

        earnings = db.query(MemberEarning).filter(
            MemberEarning.member_id.in_(member_ids),
            MemberEarning.payment_status == EarningPaymentStatus.CALCULATED.value
        ).all()

        if not earnings:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No calculated unpaid earnings available for payout")

        total_amount = sum(e.net_payable_amount for e in earnings)
        ref = f"PAY-SHG-{payout_in.shg_id}-{datetime.now(timezone.utc).strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"

        payout = Payout(
            shg_id=payout_in.shg_id,
            payout_reference=ref,
            period_start=payout_in.period_start,
            period_end=payout_in.period_end,
            total_amount=round(total_amount, 2),
            status=PayoutStatus.PENDING_GROUP_APPROVAL.value,
            notes=payout_in.notes
        )
        db.add(payout)
        
        # Mark individual earnings as PENDING_APPROVAL
        for e in earnings:
            e.payment_status = EarningPaymentStatus.PENDING_APPROVAL.value

        db.commit()
        db.refresh(payout)
        return payout

    @staticmethod
    def submit_payout_approval(
        db: Session,
        payout_id: int,
        approver_id: int,
        approval_in: PayoutApprovalRequest
    ) -> Payout:
        payout = db.query(Payout).filter(Payout.id == payout_id).first()
        if not payout:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payout record not found")

        approval = PayoutApproval(
            payout_id=payout.id,
            approver_id=approver_id,
            decision=approval_in.decision.value,
            notes=approval_in.notes,
            decided_at=datetime.now(timezone.utc)
        )
        db.add(approval)

        if approval_in.decision == ApprovalDecision.APPROVED:
            payout.status = PayoutStatus.PAYMENT_PENDING.value
            # Update member earnings to APPROVED
            members = db.query(SHGMember).filter(SHGMember.shg_id == payout.shg_id).all()
            m_ids = [m.id for m in members]
            earnings = db.query(MemberEarning).filter(
                MemberEarning.member_id.in_(m_ids),
                MemberEarning.payment_status == EarningPaymentStatus.PENDING_APPROVAL.value
            ).all()
            for e in earnings:
                e.payment_status = EarningPaymentStatus.APPROVED.value
        elif approval_in.decision == ApprovalDecision.REJECTED:
            payout.status = PayoutStatus.REJECTED.value
        else:
            payout.status = PayoutStatus.NEEDS_CORRECTION.value

        db.commit()
        db.refresh(payout)
        return payout

    @staticmethod
    def confirm_genuine_payment(
        db: Session,
        payout_id: int,
        confirm_in: PayoutPaymentConfirmation
    ) -> Payout:
        payout = db.query(Payout).filter(Payout.id == payout_id).first()
        if not payout:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payout record not found")

        if payout.status != PayoutStatus.PAYMENT_PENDING.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot record payment for payout in status '{payout.status}'. Must be in PAYMENT_PENDING."
            )

        if not confirm_in.transaction_ref or len(confirm_in.transaction_ref.strip()) < 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A genuine bank/UPI transaction reference number is strictly required."
            )

        payout.status = PayoutStatus.PAID.value
        payout.payment_method = confirm_in.payment_method
        payout.transaction_ref = confirm_in.transaction_ref
        payout.payment_date = confirm_in.payment_date
        if confirm_in.notes:
            payout.notes = f"{payout.notes or ''}\nPayment confirmation: {confirm_in.notes}".strip()

        # Update member earnings to PAID and send notification
        members = db.query(SHGMember).filter(SHGMember.shg_id == payout.shg_id).all()
        m_ids = [m.id for m in members]
        earnings = db.query(MemberEarning).filter(
            MemberEarning.member_id.in_(m_ids),
            MemberEarning.payment_status == EarningPaymentStatus.APPROVED.value
        ).all()
        
        for e in earnings:
            e.payment_status = EarningPaymentStatus.PAID.value
            notif = Notification(
                user_id=e.member.user_id,
                title="Payout Processed & Transferred",
                message=f"Your payment of ₹{e.net_payable_amount} for Order #{e.bulk_order_id} has been transferred via {confirm_in.payment_method} (Ref: {confirm_in.transaction_ref}).",
                notification_type="PAYMENT_RECEIVED",
                reference_id=payout.id,
                reference_type="Payout"
            )
            db.add(notif)

        db.commit()
        db.refresh(payout)
        return payout
