from datetime import datetime, timezone
from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.logistics import LogisticsRecord, Shipment, LogisticsStatus, ShipmentStatus
from app.models.order import BulkOrder, OrderStatus
from app.schemas.logistics import LogisticsRecordCreate, LogisticsRecordUpdate, ShipmentCreate, ShipmentUpdate


class LogisticsService:

    @staticmethod
    def create_logistics_record(db: Session, record_in: LogisticsRecordCreate) -> LogisticsRecord:
        record = LogisticsRecord(
            type=record_in.type.value,
            shg_id=record_in.shg_id,
            related_order_id=record_in.related_order_id,
            carrier_name=record_in.carrier_name,
            tracking_number=record_in.tracking_number,
            origin=record_in.origin,
            destination=record_in.destination,
            dispatch_date=record_in.dispatch_date,
            expected_delivery_date=record_in.expected_delivery_date,
            status=LogisticsStatus.SCHEDULED.value,
            remarks=record_in.remarks
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def update_logistics_record(db: Session, record_id: int, update_in: LogisticsRecordUpdate) -> LogisticsRecord:
        record = db.query(LogisticsRecord).filter(LogisticsRecord.id == record_id).first()
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Logistics record not found")

        record.status = update_in.status.value
        if update_in.actual_delivery_date:
            record.actual_delivery_date = update_in.actual_delivery_date
        if update_in.delivery_proof_document_id:
            record.delivery_proof_document_id = update_in.delivery_proof_document_id
        if update_in.remarks:
            record.remarks = f"{record.remarks or ''}\n{update_in.remarks}".strip()

        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def create_shipment(db: Session, ship_in: ShipmentCreate) -> Shipment:
        order = db.query(BulkOrder).filter(BulkOrder.id == ship_in.bulk_order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bulk order not found")

        shipment = Shipment(
            bulk_order_id=ship_in.bulk_order_id,
            shipment_number=ship_in.shipment_number,
            total_quantity=ship_in.total_quantity,
            carrier_name=ship_in.carrier_name,
            dispatch_date=ship_in.dispatch_date,
            expected_delivery_date=ship_in.expected_delivery_date,
            status=ShipmentStatus.PREPARING.value,
            delivery_notes=ship_in.delivery_notes
        )
        db.add(shipment)
        
        # Advance order status to READY_FOR_SHIPMENT if appropriate
        if order.status in [OrderStatus.QUALITY_CHECK.value, OrderStatus.IN_PRODUCTION.value]:
            order.status = OrderStatus.READY_FOR_SHIPMENT.value

        db.commit()
        db.refresh(shipment)
        return shipment

    @staticmethod
    def update_shipment_status(db: Session, shipment_id: int, update_in: ShipmentUpdate) -> Shipment:
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

        shipment.status = update_in.status.value
        if update_in.actual_delivery_date:
            shipment.actual_delivery_date = update_in.actual_delivery_date
        if update_in.delivery_notes:
            shipment.delivery_notes = f"{shipment.delivery_notes or ''}\n{update_in.delivery_notes}".strip()

        # Update parent order lifecycle status accordingly
        order = shipment.order
        if order:
            if update_in.status == ShipmentStatus.DISPATCHED:
                order.status = OrderStatus.SHIPPED.value
            elif update_in.status == ShipmentStatus.DELIVERED:
                order.status = OrderStatus.DELIVERED.value

        db.commit()
        db.refresh(shipment)
        return shipment
