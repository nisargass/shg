from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.work import WorkAllocation
from app.models.user import User
from app.schemas.allocation import (
    WorkAllocationCreate, WorkAllocationBatchCreate, WorkAllocationUpdate,
    WorkAllocationOut
)
from app.schemas.common import APIResponse
from app.services.allocation_service import AllocationService
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.get("/ai-recommendations", response_model=APIResponse[Dict[str, Any]])
def get_ai_allocation_recommendation(
    bulk_order_id: int,
    order_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Requests intelligent AI work allocation recommendations based on skills, capacity, and deadlines."""
    recommendation = AllocationService.get_ai_allocation_recommendations(
        db=db,
        bulk_order_id=bulk_order_id,
        order_item_id=order_item_id
    )
    return APIResponse(
        success=True,
        message="AI allocation recommendations generated. Ready for leader review.",
        data=recommendation
    )


@router.post("/propose", response_model=APIResponse[List[WorkAllocationOut]], status_code=status.HTTP_201_CREATED)
def propose_work_allocations(
    batch_in: WorkAllocationBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER))
):
    """Proposes batch task allocations. Enforces that total allocated does not exceed order item quantity."""
    allocations = AllocationService.propose_allocations(db=db, batch_in=batch_in)
    return APIResponse(
        success=True,
        message="Allocations proposed in PROPOSED state",
        data=[WorkAllocationOut.model_validate(a) for a in allocations]
    )


@router.put("/{allocation_id}", response_model=APIResponse[WorkAllocationOut])
def approve_or_modify_allocation(
    allocation_id: int,
    update_in: WorkAllocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER))
):
    """SHG Leader reviews, modifies quantities, or approves proposed allocations."""
    allocation = AllocationService.approve_or_modify_allocation(
        db=db,
        allocation_id=allocation_id,
        leader_id=current_user.id,
        update_in=update_in
    )
    return APIResponse(
        success=True,
        message="Allocation updated successfully",
        data=WorkAllocationOut.model_validate(allocation)
    )


@router.get("/order/{order_id}", response_model=APIResponse[List[WorkAllocationOut]])
def get_order_allocations(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Lists all work allocations for an order."""
    allocations = db.query(WorkAllocation).filter(WorkAllocation.bulk_order_id == order_id).all()
    return APIResponse(
        success=True,
        message="Work allocations retrieved",
        data=[WorkAllocationOut.model_validate(a) for a in allocations]
    )
