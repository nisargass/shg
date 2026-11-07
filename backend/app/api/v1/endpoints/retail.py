from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.retail import RetailOrder
from app.models.user import User
from app.schemas.retail import RetailOrderCreate, RetailOrderOut
from app.schemas.common import APIResponse
from app.services.retail_service import RetailService
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/orders", response_model=APIResponse[RetailOrderOut], status_code=status.HTTP_201_CREATED)
def place_retail_order(
    order_in: RetailOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.CUSTOMER, UserRole.BUYER))
):
    """Places a retail order and strictly reserves freely available stock without touching bulk reserves."""
    order = RetailService.create_retail_order(db=db, customer_id=current_user.id, order_in=order_in)
    return APIResponse(
        success=True,
        message="Retail order placed and stock reserved successfully",
        data=RetailOrderOut.model_validate(order)
    )


@router.get("/orders/my", response_model=APIResponse[List[RetailOrderOut]])
def get_my_retail_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Customer views her own retail order history."""
    orders = db.query(RetailOrder).filter(RetailOrder.customer_id == current_user.id).all()
    return APIResponse(
        success=True,
        message="Retail orders retrieved",
        data=[RetailOrderOut.model_validate(o) for o in orders]
    )
