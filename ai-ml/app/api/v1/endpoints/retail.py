from fastapi import APIRouter, Depends
from app.core.security import verify_service_key
from app.schemas.retail import RetailDemandRequest, RetailDemandResponse
from app.services.retail_service import retail_service

router = APIRouter()


@router.post(
    "/retail/forecast-demand",
    response_model=RetailDemandResponse,
    summary="Forecast retail demand",
    description="Performs statistical trend forecasting over chronological monthly sales and incorporates festive demand multipliers."
)
def forecast_demand(
    request: RetailDemandRequest,
    _auth: str = Depends(verify_service_key)
) -> RetailDemandResponse:
    """Projects monthly sales volume, standard error confidence intervals, and explains trend assumptions."""
    return retail_service.forecast_demand(request)

