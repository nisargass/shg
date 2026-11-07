import uuid
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.order import BulkOrder, OrderItem, OrderStatus, Product
from app.schemas.order import BulkOrderCreate, BulkOrderUpdate, OrderItemCreate


# Permitted lifecycle state transitions
VALID_TRANSITIONS = {
    OrderStatus.DRAFT: [OrderStatus.SUBMITTED, OrderStatus.CANCELLED],
    OrderStatus.SUBMITTED: [OrderStatus.ACCEPTED, OrderStatus.REJECTED, OrderStatus.CANCELLED],
    OrderStatus.ACCEPTED: [OrderStatus.PRICING_PENDING, OrderStatus.ALLOCATION_PENDING, OrderStatus.CANCELLED],
    OrderStatus.PRICING_PENDING: [OrderStatus.ALLOCATION_PENDING, OrderStatus.CANCELLED],
    OrderStatus.ALLOCATION_PENDING: [OrderStatus.IN_PRODUCTION, OrderStatus.CANCELLED],
    OrderStatus.IN_PRODUCTION: [OrderStatus.QUALITY_CHECK, OrderStatus.CANCELLED],
    OrderStatus.QUALITY_CHECK: [OrderStatus.READY_FOR_SHIPMENT, OrderStatus.IN_PRODUCTION, OrderStatus.CANCELLED],
    OrderStatus.READY_FOR_SHIPMENT: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
    OrderStatus.SHIPPED: [OrderStatus.DELIVERED, OrderStatus.CANCELLED],
    OrderStatus.DELIVERED: [OrderStatus.COMPLETED],
    OrderStatus.COMPLETED: [],
    OrderStatus.CANCELLED: [],
    OrderStatus.REJECTED: [],
}


class OrderService:

    @staticmethod
    def generate_order_number() -> str:
        unique_suffix = uuid.uuid4().hex[:8].upper()
        return f"ORD-SHG-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{unique_suffix}"

    @staticmethod
    def create_bulk_order(db: Session, buyer_id: int, order_in: BulkOrderCreate) -> BulkOrder:
        order_num = OrderService.generate_order_number()
        
        order = BulkOrder(
            order_number=order_num,
            buyer_id=buyer_id,
            shg_id=order_in.shg_id,
            title=order_in.title,
            description=order_in.description,
            target_delivery_date=order_in.target_delivery_date,
            currency=order_in.currency,
            notes=order_in.notes,
            status=OrderStatus.DRAFT.value
        )
        db.add(order)
        db.flush()

        total_value = 0.0
        for item_in in order_in.items:
            product = db.query(Product).filter(Product.id == item_in.product_id).first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {item_in.product_id} not found")
            
            unit_price = item_in.unit_price if item_in.unit_price > 0 else product.standard_rate
            item_total = unit_price * item_in.quantity
            total_value += item_total

            item = OrderItem(
                bulk_order_id=order.id,
                product_id=product.id,
                quantity=item_in.quantity,
                unit_price=unit_price,
                specifications=item_in.specifications,
                pending_quantity=item_in.quantity,
                completed_quantity=0
            )
            db.add(item)

        order.total_order_value = round(total_value, 2)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def transition_order_status(db: Session, order_id: int, new_status: OrderStatus, reason: Optional[str] = None) -> BulkOrder:
        order = db.query(BulkOrder).filter(BulkOrder.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        current_status = OrderStatus(order.status)
        allowed = VALID_TRANSITIONS.get(current_status, [])
        if new_status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid order status transition from {current_status.value} to {new_status.value}. Allowed: {[s.value for s in allowed]}"
            )

        order.status = new_status.value
        if reason:
            order.notes = f"{order.notes or ''}\nStatus changed to {new_status.value}: {reason}".strip()
        
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def update_order(db: Session, order_id: int, order_update: BulkOrderUpdate) -> BulkOrder:
        order = db.query(BulkOrder).filter(BulkOrder.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        if order.status not in [OrderStatus.DRAFT.value, OrderStatus.SUBMITTED.value]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order details can only be modified while in DRAFT or SUBMITTED status"
            )

        update_data = order_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(order, key, value)

        db.commit()
        db.refresh(order)
        return order
