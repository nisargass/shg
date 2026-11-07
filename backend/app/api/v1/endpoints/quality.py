from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.quality import QualityInspection
from app.models.work import ProductionBatch
from app.models.user import User
from app.schemas.quality import QualityReviewRequest, QualityInspectionOut
from app.schemas.common import APIResponse
from app.services.quality_service import QualityService
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/inspect/{inspection_id}/ai", response_model=APIResponse[QualityInspectionOut])
def trigger_ai_quality_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER, UserRole.BUYER))
):
    """Triggers computer vision defect detection and specification deviation analysis on batch photos."""
    inspection = QualityService.run_ai_inspection(db=db, inspection_id=inspection_id)
    return APIResponse(
        success=True,
        message="AI inspection completed. Inspection marked PENDING_HUMAN_REVIEW.",
        data=QualityInspectionOut.model_validate(inspection)
    )


@router.put("/inspect/{inspection_id}/decision", response_model=APIResponse[QualityInspectionOut])
def submit_human_quality_decision(
    inspection_id: int,
    review_in: QualityReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.BUYER, UserRole.FEDERATION_OFFICER))
):
    """Authorized human reviewer approves, rejects, or requests rework. (AI never makes the final decision!)."""
    inspection = QualityService.submit_human_decision(
        db=db,
        inspection_id=inspection_id,
        reviewer_id=current_user.id,
        review_in=review_in
    )
    return APIResponse(
        success=True,
        message=f"Human quality decision '{review_in.human_decision}' recorded successfully",
        data=QualityInspectionOut.model_validate(inspection)
    )


@router.get("/batch/{batch_id}", response_model=APIResponse[QualityInspectionOut])
def get_batch_inspection(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves the quality inspection record associated with a batch."""
    batch = db.query(ProductionBatch).filter(ProductionBatch.id == batch_id).first()
    if not batch or not batch.inspection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inspection record not found for batch")

    return APIResponse(
        success=True,
        message="Quality inspection details retrieved",
        data=QualityInspectionOut.model_validate(batch.inspection)
    )
