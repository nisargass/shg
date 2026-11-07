from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.finance import Payout
from app.models.user import User
from app.schemas.finance import (
    PayoutCreate, PayoutApprovalRequest, PayoutPaymentConfirmation, PayoutOut
)
from app.schemas.common import APIResponse
from app.services.payout_service import PayoutService
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/", response_model=APIResponse[PayoutOut], status_code=status.HTTP_201_CREATED)
def create_payout(
    payout_in: PayoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER))
):
    """Creates a consolidated group payout batch in PENDING_GROUP_APPROVAL status."""
    payout = PayoutService.create_group_payout(db=db, payout_in=payout_in)
    return APIResponse(
        success=True,
        message="Group payout created. Awaiting group approval decision.",
        data=PayoutOut.model_validate(payout)
    )


@router.put("/{payout_id}/approval", response_model=APIResponse[PayoutOut])
def approve_payout(
    payout_id: int,
    approval_in: PayoutApprovalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Submits group approval decision for a payout batch."""
    payout = PayoutService.submit_payout_approval(
        db=db,
        payout_id=payout_id,
        approver_id=current_user.id,
        approval_in=approval_in
    )
    return APIResponse(
        success=True,
        message=f"Payout approval recorded with status '{payout.status}'",
        data=PayoutOut.model_validate(payout)
    )


@router.put("/{payout_id}/confirm-payment", response_model=APIResponse[PayoutOut])
def confirm_payout_payment(
    payout_id: int,
    confirm_in: PayoutPaymentConfirmation,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER))
):
    """Confirms genuine disbursement with real bank/UPI transaction reference number."""
    payout = PayoutService.confirm_genuine_payment(
        db=db,
        payout_id=payout_id,
        confirm_in=confirm_in
    )
    return APIResponse(
        success=True,
        message="Genuine payment confirmed. Member earnings marked PAID.",
        data=PayoutOut.model_validate(payout)
    )


@router.get("/shg/{shg_id}", response_model=APIResponse[List[PayoutOut]])
def list_shg_payouts(
    shg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Lists payout history for an SHG."""
    payouts = db.query(Payout).filter(Payout.shg_id == shg_id).all()
    return APIResponse(
        success=True,
        message="Payout history retrieved",
        data=[PayoutOut.model_validate(p) for p in payouts]
    )
