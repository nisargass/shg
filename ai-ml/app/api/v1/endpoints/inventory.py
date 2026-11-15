from fastapi import APIRouter, Depends
from app.core.security import verify_service_key
from app.schemas.inventory import InventoryRestockRequest, InventoryRestockResponse
from app.services.inventory_service import inventory_service

router = APIRouter()


@router.post(
    "/inventory/forecast-restock",
    response_model=InventoryRestockResponse,
    summary="Forecast inventory restock and stockout alerts",
    description="Calculates usable stock after bulk reservation commitments, stockout depletion days, reorder quantity, and urgency classification."
)
def forecast_restock(
    request: InventoryRestockRequest,
    _auth: str = Depends(verify_service_key)
) -> InventoryRestockResponse:
    """Returns days until stockout, recommended replenishment order volume, and priority urgency."""
    return inventory_service.forecast_restock(request)

