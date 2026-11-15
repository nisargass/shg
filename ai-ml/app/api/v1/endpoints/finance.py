from fastapi import APIRouter, Depends
from app.core.security import verify_service_key
from app.schemas.finance import FinancialAnomalyRequest, FinancialAnomalyResponse
from app.services.finance_service import finance_service

router = APIRouter()


@router.post(
    "/finance/detect-anomalies",
    response_model=FinancialAnomalyResponse,
    summary="Detect financial payout calculation anomalies",
    description="Audits artisan earnings records for arithmetic errors, excessive deduction ratios, negative payouts, and over-production claims."
)
def detect_anomalies(
    request: FinancialAnomalyRequest,
    _auth: str = Depends(verify_service_key)
) -> FinancialAnomalyResponse:
    """Returns detected discrepancy flags, severity ratings, and flags records requiring human resolution."""
    return finance_service.detect_anomalies(request)

