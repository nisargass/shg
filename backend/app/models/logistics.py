from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class LogisticsType(str, Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"


class LogisticsStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    DISPATCHED = "DISPATCHED"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    DELAYED = "DELAYED"


class ShipmentStatus(str, Enum):
    PREPARING = "PREPARING"
    DISPATCHED = "DISPATCHED"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    RETURNED = "RETURNED"


class LogisticsRecord(Base):
    __tablename__ = "logistics_records"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), default=LogisticsType.OUTBOUND.value, nullable=False, index=True)
    shg_id = Column(Integer, ForeignKey("shgs.id"), nullable=False, index=True)
    related_order_id = Column(Integer, nullable=True, index=True)
    carrier_name = Column(String(255), nullable=True)
    tracking_number = Column(String(100), nullable=True, index=True)
    origin = Column(String(255), nullable=True)
    destination = Column(String(255), nullable=True)
    dispatch_date = Column(DateTime, nullable=True)
    expected_delivery_date = Column(DateTime, nullable=True)
    actual_delivery_date = Column(DateTime, nullable=True)
    status = Column(String(50), default=LogisticsStatus.SCHEDULED.value, nullable=False, index=True)
    delivery_proof_document_id = Column(Integer, nullable=True)
    remarks = Column(Text, nullable=True)


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    bulk_order_id = Column(Integer, ForeignKey("bulk_orders.id"), nullable=False, index=True)
    shipment_number = Column(String(100), unique=True, index=True, nullable=False)
    total_quantity = Column(Integer, nullable=False)
    carrier_name = Column(String(255), nullable=True)
    dispatch_date = Column(DateTime, nullable=True)
    expected_delivery_date = Column(DateTime, nullable=True)
    actual_delivery_date = Column(DateTime, nullable=True)
    status = Column(String(50), default=ShipmentStatus.PREPARING.value, nullable=False, index=True)
    delivery_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    order = relationship("BulkOrder", back_populates="shipments")
