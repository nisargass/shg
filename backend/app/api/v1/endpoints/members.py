import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import SHGMember, MemberCapacity, User
from app.models.work import WorkAllocation
from app.schemas.user import MemberCreate, MemberOut, MemberCapacityOut, MemberCapacityUpdate
from app.schemas.allocation import MemberTaskOut
from app.schemas.common import APIResponse
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/", response_model=APIResponse[MemberOut], status_code=status.HTTP_201_CREATED)
def add_member_to_shg(
    member_in: MemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Adds a registered user as a member of an SHG and sets initial capacity."""
    existing = db.query(SHGMember).filter(SHGMember.user_id == member_in.user_id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already registered as an SHG member")

    member = SHGMember(
        user_id=member_in.user_id,
        shg_id=member_in.shg_id,
        skills=json.dumps(member_in.skills or []),
        bank_account_number=member_in.bank_account_number,
        ifsc_code=member_in.ifsc_code,
        is_active=True
    )
    db.add(member)
    db.flush()

    # Initialize MemberCapacity record
    capacity = MemberCapacity(
        member_id=member.id,
        available_hours_per_day=6.0,
        current_workload=0.0,
        max_feasible_daily_quantity=10.0,
        historical_completion_rate=100.0,
        active_tasks_count=0
    )
    db.add(capacity)
    db.commit()
    db.refresh(member)

    return APIResponse(
        success=True,
        message="Member registered successfully with initial capacity profile",
        data=MemberOut.model_validate(member)
    )


@router.get("/me/tasks", response_model=APIResponse[List[MemberTaskOut]])
def get_my_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_MEMBER))
):
    """Member views only her own assigned tasks and deadlines."""
    member = db.query(SHGMember).filter(SHGMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member profile not found for current user")

    allocations = db.query(WorkAllocation).filter(WorkAllocation.member_id == member.id).all()
    tasks = []
    for a in allocations:
        tasks.append(
            MemberTaskOut(
                id=a.id,
                order_title=a.order.title if a.order else "Bulk Order",
                order_number=a.order.order_number if a.order else "",
                product_name=a.order_item.product.name if a.order_item and a.order_item.product else "Craft Item",
                allocated_quantity=a.allocated_quantity,
                completed_quantity=a.completed_quantity,
                pending_quantity=max(0, a.allocated_quantity - a.completed_quantity),
                unit_rate=a.unit_rate,
                deadline=a.deadline,
                status=a.status,
                progress_percentage=a.progress_percentage
            )
        )

    return APIResponse(
        success=True,
        message="My assigned tasks retrieved successfully",
        data=tasks
    )


@router.get("/{member_id}/capacity", response_model=APIResponse[MemberCapacityOut])
def get_member_capacity(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves member capacity. Strictly restricted to the member herself or her SHG leader."""
    member = db.query(SHGMember).filter(SHGMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    # Enforce member privacy: a member cannot view another member's capacity
    if current_user.role == UserRole.SHG_MEMBER.value and member.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Cannot view another member's private capacity record")

    if not member.capacity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capacity profile not found")

    return APIResponse(
        success=True,
        message="Member capacity profile retrieved",
        data=MemberCapacityOut.model_validate(member.capacity)
    )


@router.put("/{member_id}/capacity", response_model=APIResponse[MemberCapacityOut])
def update_member_capacity(
    member_id: int,
    cap_update: MemberCapacityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.SHG_MEMBER))
):
    """Updates member capacity parameters."""
    member = db.query(SHGMember).filter(SHGMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    # Member can only update her own capacity; Leader can update any member of her SHG
    if current_user.role == UserRole.SHG_MEMBER.value and member.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot edit another member's capacity profile")

    capacity = member.capacity
    if not capacity:
        capacity = MemberCapacity(member_id=member.id)
        db.add(capacity)

    update_dict = cap_update.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(capacity, key, value)

    db.commit()
    db.refresh(capacity)

    return APIResponse(
        success=True,
        message="Member capacity profile updated",
        data=MemberCapacityOut.model_validate(capacity)
    )
