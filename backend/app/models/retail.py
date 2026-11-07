from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class RetailOrderStatus(str, Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class RetailOrder(Base):
    __tablename__ = "retail_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), default=RetailOrderStatus.PLACED.value, nullable=False, index=True)
    shipping_address = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    customer = relationship("User", foreign_keys=[customer_id])
    items = relationship("RetailOrderItem", back_populates="retail_order", cascade="all, delete-orphan")


class RetailOrderItem(Base):
    __tablename__ = "retail_order_items"

    id = Column(Integer, primary_key=True, index=True)
    retail_order_id = Column(Integer, ForeignKey("retail_orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    # Relationships
    retail_order = relationship("RetailOrder", back_populates="items")
    product = relationship("Product", back_populates="retail_order_items")
