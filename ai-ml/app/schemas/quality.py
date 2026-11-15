from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SpecificationInput(BaseModel):
    parameter_name: str
    target_value: str
    tolerance_range: Optional[str] = "Exact"


class QualityInspectionRequest(BaseModel):
    batch_id: int
    product_id: int
    photo_urls: List[str] = Field(..., min_length=1, description="URLs or local paths of batch photos")
    specifications: List[SpecificationInput] = Field(default_factory=list)


class DefectItem(BaseModel):
    type: str
    location: str
    severity: str = "LOW"  # LOW, MEDIUM, HIGH


class SpecificationDeviation(BaseModel):
    parameter_name: str
    observed_value: str
    status: str = "DEVIATION"


class QualityInspectionResponse(BaseModel):
    success: bool = True
    batch_id: int
    quality_score: float = Field(..., description="Quality score between 0.0 and 100.0 (or normalized 0.0-1.0)")
    confidence_score: float = Field(..., description="Visual model confidence 0.0 to 1.0")
    detected_issues: List[str] = Field(default_factory=list, description="Human readable list of detected visual issues")
    defects_detected: List[DefectItem] = []
    specification_deviations: List[SpecificationDeviation] = []
    explanation: str
    suggested_action: str = Field(..., description="e.g. HUMAN_REVIEW, LOW_IMAGE_QUALITY, TRIM_AND_APPROVE, REWORK_REQUIRED")
    review_required: bool = Field(True, description="Human inspector sign-off is always mandatory")
    image_quality_status: str = Field("ACCEPTABLE", description="ACCEPTABLE, LOW_IMAGE_QUALITY, or UNREADABLE")
