from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class InventoryItemType(str, Enum):
    RAW_MATERIAL = "RAW_MATERIAL"
    WIP = "WIP"
    FINISHED_GOOD = "FINISHED_GOOD"


class ReservationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    FULFILLED = "FULFILLED"
    RELEASED = "RELEASED"


class PurchaseStatus(str, Enum):
    ORDERED = "ORDERED"
    RECEIVED = "RECEIVED"
    PARTIALLY_RECEIVED = "PARTIALLY_RECEIVED"
    CANCELLED = "CANCELLED"


class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    shg_id = Column(Integer, ForeignKey("shgs.id"), nullable=False, index=True)
    item_type = Column(String(50), default=InventoryItemType.RAW_MATERIAL.value, nullable=False, index=True)
    item_name = Column(String(255), nullable=False, index=True)
    unit = Column(String(50), default="kg")
    
    # Stock Quantities
    physical_stock = Column(Float, nullable=False, default=0.0)
    bulk_reserved_stock = Column(Float, nullable=False, default=0.0)
    retail_reserved_stock = Column(Float, nullable=False, default=0.0)
    damaged_stock = Column(Float, nullable=False, default=0.0)
    
    unit_cost = Column(Float, default=0.0)
    low_stock_threshold = Column(Float, default=10.0)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    shg = relationship("SHG", back_populates="inventory_items")
    reservations = relationship("InventoryReservation", back_populates="inventory", cascade="all, delete-orphan")

    @property
    def available_stock(self) -> float:
        """Physical stock - bulk reserved - retail reserved - damaged stock."""
        avail = self.physical_stock - self.bulk_reserved_stock - self.retail_reserved_stock - self.damaged_stock
        return max(0.0, round(avail, 2))


class InventoryReservation(Base):
    __tablename__ = "inventory_reservations"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventories.id"), nullable=False, index=True)
    order_type = Column(String(20), nullable=False)  # BULK or RETAIL
    order_id = Column(Integer, nullable=False, index=True)
    reserved_quantity = Column(Float, nullable=False)
    status = Column(String(50), default=ReservationStatus.ACTIVE.value, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    inventory = relationship("Inventory", back_populates="reservations")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    contact_person = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    materials_supplied = Column(Text, nullable=True, default="[]")  # JSON string
    reliability_score = Column(Float, default=100.0)  # percentage
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    purchases = relationship("MaterialPurchase", back_populates="supplier")


class MaterialPurchase(Base):
    __tablename__ = "material_purchases"

    id = Column(Integer, primary_key=True, index=True)
    shg_id = Column(Integer, ForeignKey("shgs.id"), nullable=False, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False, index=True)
    material_name = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50), default="kg")
    unit_price = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    purchase_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String(50), default=PurchaseStatus.ORDERED.value, nullable=False, index=True)
    received_date = Column(DateTime, nullable=True)
    shortage_or_damage_notes = Column(Text, nullable=True)
    invoice_document_id = Column(Integer, nullable=True)

    # Relationships
    supplier = relationship("Supplier", back_populates="purchases")
