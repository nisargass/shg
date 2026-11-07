from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.quality import QualityStatus


class QualityInspectionCreate(BaseModel):
    production_batch_id: int


class QualityReviewRequest(BaseModel):
    human_decision: str = Field(..., description="APPROVED, REJECTED, or REWORK_REQUIRED")
    rejection_reason: Optional[str] = None


class QualityInspectionOut(BaseModel):
    id: int
    production_batch_id: int
    inspector_id: Optional[int] = None
    status: QualityStatus
    ai_score: Optional[float] = None
    ai_defects_detected: Optional[str] = "[]"
    ai_explanation: Optional[str] = None
    ai_suggested_action: Optional[str] = None
    human_decision: Optional[str] = None
    human_reviewer_id: Optional[int] = None
    rejection_reason: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
