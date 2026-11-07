from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.logistics import LogisticsType, LogisticsStatus, ShipmentStatus


class LogisticsRecordCreate(BaseModel):
    type: LogisticsType = LogisticsType.OUTBOUND
    shg_id: int
    related_order_id: Optional[int] = None
    carrier_name: Optional[str] = None
    tracking_number: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    dispatch_date: Optional[datetime] = None
    expected_delivery_date: Optional[datetime] = None
    remarks: Optional[str] = None


class LogisticsRecordUpdate(BaseModel):
    status: LogisticsStatus
    actual_delivery_date: Optional[datetime] = None
    delivery_proof_document_id: Optional[int] = None
    remarks: Optional[str] = None


class LogisticsRecordOut(BaseModel):
    id: int
    type: LogisticsType
    shg_id: int
    related_order_id: Optional[int] = None
    carrier_name: Optional[str] = None
    tracking_number: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    dispatch_date: Optional[datetime] = None
    expected_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    status: LogisticsStatus
    delivery_proof_document_id: Optional[int] = None
    remarks: Optional[str] = None

    class Config:
        from_attributes = True


class ShipmentCreate(BaseModel):
    bulk_order_id: int
    shipment_number: str
    total_quantity: int
    carrier_name: Optional[str] = None
    dispatch_date: Optional[datetime] = None
    expected_delivery_date: Optional[datetime] = None
    delivery_notes: Optional[str] = None


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus
    actual_delivery_date: Optional[datetime] = None
    delivery_notes: Optional[str] = None


class ShipmentOut(BaseModel):
    id: int
    bulk_order_id: int
    shipment_number: str
    total_quantity: int
    carrier_name: Optional[str] = None
    dispatch_date: Optional[datetime] = None
    expected_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    status: ShipmentStatus
    delivery_notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
