from datetime import datetime, timezone
from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.inventory import Inventory, InventoryReservation, ReservationStatus, InventoryItemType
from app.models.support import Notification
from app.schemas.inventory import InventoryCreate, InventoryUpdate, ReservationCreate


class InventoryService:

    @staticmethod
    def create_inventory_item(db: Session, item_in: InventoryCreate) -> Inventory:
        item = Inventory(
            shg_id=item_in.shg_id,
            item_type=item_in.item_type.value,
            item_name=item_in.item_name,
            unit=item_in.unit,
            physical_stock=item_in.physical_stock,
            bulk_reserved_stock=0.0,
            retail_reserved_stock=0.0,
            damaged_stock=0.0,
            unit_cost=item_in.unit_cost,
            low_stock_threshold=item_in.low_stock_threshold
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_stock(db: Session, inventory_id: int, update_in: InventoryUpdate) -> Inventory:
        item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")

        if update_in.physical_stock is not None:
            if update_in.physical_stock < (item.bulk_reserved_stock + item.retail_reserved_stock):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Physical stock cannot be set lower than currently committed reservations"
                )
            item.physical_stock = update_in.physical_stock

        if update_in.damaged_stock is not None:
            item.damaged_stock = update_in.damaged_stock

        if update_in.unit_cost is not None:
            item.unit_cost = update_in.unit_cost

        if update_in.low_stock_threshold is not None:
            item.low_stock_threshold = update_in.low_stock_threshold

        # Check for low-stock alert
        if item.available_stock <= item.low_stock_threshold:
            if item.shg and item.shg.leader_id:
                notif = Notification(
                    user_id=item.shg.leader_id,
                    title="Low Stock Alert",
                    message=f"Available stock for '{item.item_name}' is {item.available_stock} {item.unit}, which is at or below threshold ({item.low_stock_threshold}).",
                    notification_type="LOW_STOCK",
                    reference_id=item.id,
                    reference_type="Inventory"
                )
                db.add(notif)

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def reserve_stock(db: Session, res_in: ReservationCreate) -> InventoryReservation:
        item = db.query(Inventory).filter(Inventory.id == res_in.inventory_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")

        order_type_upper = res_in.order_type.upper()
        if order_type_upper not in ["BULK", "RETAIL"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order type must be BULK or RETAIL")

        # Check available stock
        # Available = physical - bulk_reserved - retail_reserved - damaged
        if res_in.reserved_quantity > item.available_stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient freely available stock for reservation. Requested: {res_in.reserved_quantity}, Available: {item.available_stock}"
            )

        # Allocate to respective reserved pool
        if order_type_upper == "BULK":
            item.bulk_reserved_stock += res_in.reserved_quantity
        else:
            # Retail order reservation strictly respects bulk reservation barrier!
            item.retail_reserved_stock += res_in.reserved_quantity

        reservation = InventoryReservation(
            inventory_id=item.id,
            order_type=order_type_upper,
            order_id=res_in.order_id,
            reserved_quantity=res_in.reserved_quantity,
            status=ReservationStatus.ACTIVE.value
        )
        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        db.refresh(item)
        return reservation

    @staticmethod
    def release_reservation(db: Session, reservation_id: int) -> InventoryReservation:
        res = db.query(InventoryReservation).filter(InventoryReservation.id == reservation_id).first()
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")

        if res.status != ReservationStatus.ACTIVE.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reservation is not currently active")

        item = res.inventory
        if res.order_type == "BULK":
            item.bulk_reserved_stock = max(0.0, item.bulk_reserved_stock - res.reserved_quantity)
        else:
            item.retail_reserved_stock = max(0.0, item.retail_reserved_stock - res.reserved_quantity)

        res.status = ReservationStatus.RELEASED.value
        db.commit()
        db.refresh(res)
        db.refresh(item)
        return res
