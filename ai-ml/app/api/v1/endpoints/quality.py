from fastapi import APIRouter, Depends
from app.core.security import verify_service_key
from app.schemas.quality import QualityInspectionRequest, QualityInspectionResponse
from app.services.quality_service import quality_service

router = APIRouter()


@router.post(
    "/quality/inspect-batch",
    response_model=QualityInspectionResponse,
    summary="Computer vision quality inspection for production batches",
    description="Inspects batch photographs against product technical specifications, identifying visual anomalies and defect severity."
)
def inspect_batch(
    request: QualityInspectionRequest,
    _auth: str = Depends(verify_service_key)
) -> QualityInspectionResponse:
    """Analyzes photo quality, resolution, edge uniformity, and returns advisory quality score."""
    return quality_service.inspect_batch(request)

