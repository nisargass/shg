from fastapi import APIRouter, Depends
from app.core.security import verify_service_key
from app.schemas.workforce import WorkforceLikelihoodRequest, WorkforceLikelihoodResponse
from app.services.workforce_service import workforce_service

router = APIRouter()


@router.post(
    "/workforce/completion-likelihood",
    response_model=WorkforceLikelihoodResponse,
    summary="Predict worker completion likelihood",
    description="Estimates whether an SHG member can complete assigned production before deadline based on workload, capacity, and historical completion."
)
def predict_completion_likelihood(
    request: WorkforceLikelihoodRequest,
    _auth: str = Depends(verify_service_key)
) -> WorkforceLikelihoodResponse:
    """Returns completion probability, estimated finish date, and key contributing factors."""
    return workforce_service.predict_completion_likelihood(request)

