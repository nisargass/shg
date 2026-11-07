from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.work import ProductionRecord, ProductionBatch, WorkAllocation
from app.models.user import User, SHGMember
from app.schemas.production import (
    ProductionRecordCreate, ProductionRecordOut,
    ProductionBatchCreate, ProductionBatchOut
)
from app.schemas.common import APIResponse
from app.services.production_service import ProductionService
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/progress", response_model=APIResponse[ProductionRecordOut], status_code=status.HTTP_201_CREATED)
def record_progress(
    record_in: ProductionRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_MEMBER))
):
    """SHG Member logs verified daily production progress, shortage, or delay."""
    member = db.query(SHGMember).filter(SHGMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member profile not found")

    record = ProductionService.record_production_progress(
        db=db,
        member_id=member.id,
        record_in=record_in
    )
    return APIResponse(
        success=True,
        message="Production progress logged and verified progress updated",
        data=ProductionRecordOut.model_validate(record)
    )


@router.post("/batch", response_model=APIResponse[ProductionBatchOut], status_code=status.HTTP_201_CREATED)
def submit_batch(
    batch_in: ProductionBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_MEMBER))
):
    """SHG Member submits a completed batch with photos for quality inspection."""
    member = db.query(SHGMember).filter(SHGMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member profile not found")

    batch = ProductionService.submit_production_batch(
        db=db,
        member_id=member.id,
        batch_in=batch_in
    )
    return APIResponse(
        success=True,
        message="Production batch submitted. Quality inspection scheduled.",
        data=ProductionBatchOut.model_validate(batch)
    )


@router.get("/allocation/{allocation_id}/records", response_model=APIResponse[List[ProductionRecordOut]])
def get_allocation_records(
    allocation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lists production progress records for a task allocation."""
    alloc = db.query(WorkAllocation).filter(WorkAllocation.id == allocation_id).first()
    if not alloc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allocation not found")

    # Member privacy: cannot view another member's logs
    if current_user.role == UserRole.SHG_MEMBER.value:
        member = db.query(SHGMember).filter(SHGMember.user_id == current_user.id).first()
        if not member or member.id != alloc.member_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot access another member's production records")

    records = db.query(ProductionRecord).filter(ProductionRecord.work_allocation_id == allocation_id).all()
    return APIResponse(
        success=True,
        message="Production records retrieved",
        data=[ProductionRecordOut.model_validate(r) for r in records]
    )
