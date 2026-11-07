from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.order import BulkOrder, OrderItem, Product, ProductSpecification, OrderStatus
from app.models.user import User, Buyer, SHG
from app.schemas.order import (
    BulkOrderCreate, BulkOrderUpdate, BulkOrderOut,
    OrderStatusTransition, ProductCreate, ProductOut, ProductSpecificationCreate, ProductSpecificationOut
)
from app.schemas.common import APIResponse
from app.services.order_service import OrderService
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/", response_model=APIResponse[BulkOrderOut], status_code=status.HTTP_201_CREATED)
def create_bulk_order(
    order_in: BulkOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.BUYER, UserRole.SHG_LEADER))
):
    """Creates a new bulk order."""
    buyer_id = None
    if current_user.role == UserRole.BUYER.value:
        buyer = db.query(Buyer).filter(Buyer.user_id == current_user.id).first()
        if not buyer:
            buyer = Buyer(user_id=current_user.id, organization_name="Independent Buyer")
            db.add(buyer)
            db.commit()
            db.refresh(buyer)
        buyer_id = buyer.id
    else:
        # Default buyer ID 1 or first available
        first_buyer = db.query(Buyer).first()
        if not first_buyer:
            first_buyer = Buyer(user_id=current_user.id, organization_name="Direct Bulk Procurement")
            db.add(first_buyer)
            db.commit()
            db.refresh(first_buyer)
        buyer_id = first_buyer.id

    order = OrderService.create_bulk_order(db=db, buyer_id=buyer_id, order_in=order_in)
    return APIResponse(
        success=True,
        message="Bulk order created successfully in DRAFT status",
        data=BulkOrderOut.model_validate(order)
    )


@router.get("/", response_model=APIResponse[List[BulkOrderOut]])
def list_bulk_orders(
    status_filter: Optional[OrderStatus] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lists bulk orders visible to the requesting user's role."""
    query = db.query(BulkOrder)

    if current_user.role == UserRole.BUYER.value and current_user.buyer_profile:
        query = query.filter(BulkOrder.buyer_id == current_user.buyer_profile.id)
    elif current_user.role == UserRole.SHG_LEADER.value and current_user.shg_led:
        shg_ids = [s.id for s in current_user.shg_led]
        query = query.filter(BulkOrder.shg_id.in_(shg_ids))

    if status_filter:
        query = query.filter(BulkOrder.status == status_filter.value)

    orders = query.all()
    return APIResponse(
        success=True,
        message="Bulk orders retrieved successfully",
        data=[BulkOrderOut.model_validate(o) for o in orders]
    )


@router.get("/{order_id}", response_model=APIResponse[BulkOrderOut])
def get_bulk_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves full details of a specific bulk order."""
    order = db.query(BulkOrder).filter(BulkOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bulk order not found")

    return APIResponse(
        success=True,
        message="Order retrieved successfully",
        data=BulkOrderOut.model_validate(order)
    )


@router.put("/{order_id}", response_model=APIResponse[BulkOrderOut])
def update_bulk_order(
    order_id: int,
    order_update: BulkOrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.BUYER, UserRole.SHG_LEADER))
):
    """Updates order details while in DRAFT or SUBMITTED status."""
    order = OrderService.update_order(db=db, order_id=order_id, order_update=order_update)
    return APIResponse(
        success=True,
        message="Bulk order updated successfully",
        data=BulkOrderOut.model_validate(order)
    )


@router.post("/{order_id}/transition", response_model=APIResponse[BulkOrderOut])
def transition_order_status(
    order_id: int,
    transition: OrderStatusTransition,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.BUYER, UserRole.FEDERATION_OFFICER))
):
    """Transitions the order status according to the validated lifecycle rules."""
    order = OrderService.transition_order_status(
        db=db,
        order_id=order_id,
        new_status=transition.new_status,
        reason=transition.reason
    )
    return APIResponse(
        success=True,
        message=f"Order status transitioned to {transition.new_status.value}",
        data=BulkOrderOut.model_validate(order)
    )


# Product catalog endpoints
@router.post("/products", response_model=APIResponse[ProductOut], status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Adds a product to the catalog."""
    product = Product(
        name=product_in.name,
        category=product_in.category,
        description=product_in.description,
        base_unit=product_in.base_unit,
        standard_rate=product_in.standard_rate,
        images=product_in.images,
        is_active=True
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return APIResponse(
        success=True,
        message="Product created successfully",
        data=ProductOut.model_validate(product)
    )


@router.get("/products/catalog", response_model=APIResponse[List[ProductOut]])
def get_product_catalog(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Returns active products in the public catalog."""
    query = db.query(Product).filter(Product.is_active == True)
    if category:
        query = query.filter(Product.category == category)
    products = query.all()
    return APIResponse(
        success=True,
        message="Product catalog retrieved",
        data=[ProductOut.model_validate(p) for p in products]
    )
