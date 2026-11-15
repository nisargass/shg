from fastapi import APIRouter, Depends
from app.core.security import verify_service_key
from app.schemas.pricing import PricingRequest, PricingResponse
from app.services.pricing_service import pricing_service

router = APIRouter()


@router.post(
    "/pricing/recommend",
    response_model=PricingResponse,
    summary="Recommend sustainable product pricing",
    description="Calculates unit selling price based on material, artisan labor, packaging, transit, and operations, checking for omitted cost overheads."
)
def recommend_pricing(
    request: PricingRequest,
    _auth: str = Depends(verify_service_key)
) -> PricingResponse:
    """Computes recommended selling price per unit, total order value, estimated net profit, and overhead warnings."""
    return pricing_service.recommend_pricing(request)

