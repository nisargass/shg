from fastapi import APIRouter, Depends
from app.core.security import verify_service_key
from app.schemas.allocation import AllocationRequest, AllocationResponse
from app.services.allocation_service import allocation_service

router = APIRouter()


@router.post(
    "/allocation/recommend",
    response_model=AllocationResponse,
    summary="Recommend intelligent and fair work allocation",
    description="Proposes an equitable distribution of production units among available members, respecting hard daily capacity bounds and skill requirements."
)
def recommend_allocation(
    request: AllocationRequest,
    _auth: str = Depends(verify_service_key)
) -> AllocationResponse:
    """Calculates fair task allocations, individual member predictions, and Jain's fairness index."""
    return allocation_service.recommend_allocation(request)

