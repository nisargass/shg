from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class OrderStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    PRICING_PENDING = "PRICING_PENDING"
    ALLOCATION_PENDING = "ALLOCATION_PENDING"
    IN_PRODUCTION = "IN_PRODUCTION"
    QUALITY_CHECK = "QUALITY_CHECK"
    READY_FOR_SHIPMENT = "READY_FOR_SHIPMENT"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    base_unit = Column(String(50), default="piece")
    standard_rate = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    images = Column(Text, nullable=True, default="[]")  # JSON array of URLs
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    order_items = relationship("OrderItem", back_populates="product")
    specifications = relationship("ProductSpecification", back_populates="product")
    retail_order_items = relationship("RetailOrderItem", back_populates="product")


class BulkOrder(Base):
    __tablename__ = "bulk_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, index=True, nullable=False)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False, index=True)
    shg_id = Column(Integer, ForeignKey("shgs.id"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default=OrderStatus.DRAFT.value, nullable=False, index=True)
    target_delivery_date = Column(DateTime, nullable=True)
    total_order_value = Column(Float, default=0.0)
    approved_price_per_unit = Column(Float, default=0.0)
    currency = Column(String(10), default="INR")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    buyer = relationship("Buyer", back_populates="orders")
    shg = relationship("SHG", back_populates="bulk_orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    pricing_breakdowns = relationship("PricingBreakdown", back_populates="order", cascade="all, delete-orphan")
    work_allocations = relationship("WorkAllocation", back_populates="order", cascade="all, delete-orphan")
    production_batches = relationship("ProductionBatch", back_populates="order")
    shipments = relationship("Shipment", back_populates="order")
    earnings = relationship("MemberEarning", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    bulk_order_id = Column(Integer, ForeignKey("bulk_orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, default=0.0)
    specifications = Column(Text, nullable=True)
    completed_quantity = Column(Integer, default=0)
    pending_quantity = Column(Integer, default=0)

    # Relationships
    order = relationship("BulkOrder", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    allocations = relationship("WorkAllocation", back_populates="order_item")


class ProductSpecification(Base):
    __tablename__ = "product_specifications"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    bulk_order_id = Column(Integer, ForeignKey("bulk_orders.id"), nullable=True, index=True)
    parameter_name = Column(String(100), nullable=False)
    target_value = Column(String(100), nullable=False)
    tolerance_range = Column(String(100), nullable=True)
    inspection_guide = Column(Text, nullable=True)

    # Relationships
    product = relationship("Product", back_populates="specifications")
