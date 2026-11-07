from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.pricing import PricingBreakdown
from app.models.user import User
from app.schemas.pricing import PricingBreakdownCreate, PricingApprovalRequest, PricingBreakdownOut
from app.schemas.common import APIResponse
from app.services.pricing_service import PricingService
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/", response_model=APIResponse[PricingBreakdownOut], status_code=status.HTTP_201_CREATED)
def create_order_pricing(
    pricing_in: PricingBreakdownCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Calculates comprehensive order costing including material, labor, packaging, transport, and margin."""
    pricing = PricingService.calculate_and_create_pricing(db=db, pricing_in=pricing_in)
    return APIResponse(
        success=True,
        message="Costing calculated successfully. Awaiting leader approval.",
        data=PricingBreakdownOut.model_validate(pricing)
    )


@router.put("/{pricing_id}/approve", response_model=APIResponse[PricingBreakdownOut])
def approve_pricing(
    pricing_id: int,
    approval_in: PricingApprovalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER))
):
    """SHG Leader reviews and officially approves the pricing structure."""
    pricing = PricingService.approve_pricing(
        db=db,
        pricing_id=pricing_id,
        approver_id=current_user.id,
        approval_in=approval_in
    )
    return APIResponse(
        success=True,
        message="Pricing decision recorded successfully",
        data=PricingBreakdownOut.model_validate(pricing)
    )


@router.get("/order/{order_id}", response_model=APIResponse[List[PricingBreakdownOut]])
def get_order_pricing_history(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER, UserRole.BUYER))
):
    """Retrieves all pricing breakdowns recorded for an order."""
    pricing_list = db.query(PricingBreakdown).filter(PricingBreakdown.bulk_order_id == order_id).all()
    return APIResponse(
        success=True,
        message="Pricing breakdowns retrieved",
        data=[PricingBreakdownOut.model_validate(p) for p in pricing_list]
    )
