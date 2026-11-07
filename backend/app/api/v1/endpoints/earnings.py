from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.finance import MemberEarning
from app.models.user import User, SHGMember
from app.schemas.finance import MemberEarningOut
from app.schemas.common import APIResponse
from app.services.payout_service import PayoutService
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/calculate/{allocation_id}", response_model=APIResponse[MemberEarningOut])
def calculate_task_earnings(
    allocation_id: int,
    deductions: float = 0.0,
    deductions_reason: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER))
):
    """Calculates member earnings from verified accepted batch quantities and approved rate."""
    earning = PayoutService.calculate_member_earnings_for_allocation(
        db=db,
        work_allocation_id=allocation_id,
        deductions=deductions,
        deductions_reason=deductions_reason
    )
    return APIResponse(
        success=True,
        message="Member earnings calculated and recorded",
        data=MemberEarningOut.model_validate(earning)
    )


@router.get("/me", response_model=APIResponse[List[MemberEarningOut]])
def get_my_earnings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_MEMBER))
):
    """Strict privacy: Member views ONLY her own earnings and payout history."""
    member = db.query(SHGMember).filter(SHGMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member profile not found")

    my_earnings = db.query(MemberEarning).filter(MemberEarning.member_id == member.id).all()
    return APIResponse(
        success=True,
        message="Personal verified earnings retrieved",
        data=[MemberEarningOut.model_validate(e) for e in my_earnings]
    )


@router.get("/member/{member_id}", response_model=APIResponse[List[MemberEarningOut]])
def get_member_earnings_by_leader(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Authorized SHG Leader / Federation Officer views member earnings breakdown."""
    member = db.query(SHGMember).filter(SHGMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    earnings = db.query(MemberEarning).filter(MemberEarning.member_id == member_id).all()
    return APIResponse(
        success=True,
        message="Member earnings retrieved for authorized leader review",
        data=[MemberEarningOut.model_validate(e) for e in earnings]
    )
