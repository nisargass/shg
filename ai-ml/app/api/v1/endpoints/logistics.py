from fastapi import APIRouter, Depends
from app.core.security import verify_service_key
from app.schemas.logistics import LogisticsRequest, LogisticsResponse
from app.services.logistics_service import logistics_service

router = APIRouter()


@router.post(
    "/logistics/recommend-route",
    response_model=LogisticsResponse,
    summary="Recommend logistics and shipping routes",
    description="Validates Indian PIN codes, determines geographical transit distances, and estimates shipping options across cost, speed, and reliability."
)
def recommend_route(
    request: LogisticsRequest,
    _auth: str = Depends(verify_service_key)
) -> LogisticsResponse:
    """Returns candidate shipping carriers (State Cargo, Postal Parcel, Express Surface) with transit hours and cost estimates."""
    return logistics_service.recommend_route(request)

