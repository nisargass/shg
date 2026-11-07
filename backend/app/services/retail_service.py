import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.retail import RetailOrder, RetailOrderItem, RetailOrderStatus
from app.models.order import Product
from app.models.inventory import Inventory, InventoryItemType
from app.schemas.retail import RetailOrderCreate
from app.services.inventory_service import InventoryService
from app.schemas.inventory import ReservationCreate


class RetailService:

    @staticmethod
    def create_retail_order(db: Session, customer_id: int, order_in: RetailOrderCreate) -> RetailOrder:
        if not order_in.items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must contain at least one item")

        order_num = f"RET-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        retail_order = RetailOrder(
            order_number=order_num,
            customer_id=customer_id,
            shipping_address=order_in.shipping_address,
            status=RetailOrderStatus.PLACED.value,
            total_amount=0.0
        )
        db.add(retail_order)
        db.flush()

        total_amount = 0.0

        for item_in in order_in.items:
            product = db.query(Product).filter(Product.id == item_in.product_id, Product.is_active == True).first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product #{item_in.product_id} not found or inactive")

            # Check inventory for finished good
            inventory_item = db.query(Inventory).filter(
                Inventory.item_name == product.name,
                Inventory.item_type == InventoryItemType.FINISHED_GOOD.value
            ).first()

            if not inventory_item:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No finished goods inventory registered for '{product.name}'"
                )

            # Strict check: Can only reserve freely available stock!
            # Available stock = physical - bulk_reserved - retail_reserved - damaged
            if inventory_item.available_stock < item_in.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient available retail stock for '{product.name}'. Available: {inventory_item.available_stock}, Requested: {item_in.quantity}"
                )

            # Reserve stock for retail order
            InventoryService.reserve_stock(
                db=db,
                res_in=ReservationCreate(
                    inventory_id=inventory_item.id,
                    order_type="RETAIL",
                    order_id=retail_order.id,
                    reserved_quantity=float(item_in.quantity)
                )
            )

            unit_price = product.standard_rate
            item_total = unit_price * item_in.quantity
            total_amount += item_total

            order_item = RetailOrderItem(
                retail_order_id=retail_order.id,
                product_id=product.id,
                quantity=item_in.quantity,
                unit_price=unit_price
            )
            db.add(order_item)

        retail_order.total_amount = round(total_amount, 2)
        db.commit()
        db.refresh(retail_order)
        return retail_order
