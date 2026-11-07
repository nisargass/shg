from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.models.order import OrderStatus


class ProductSpecificationCreate(BaseModel):
    parameter_name: str
    target_value: str
    tolerance_range: Optional[str] = None
    inspection_guide: Optional[str] = None


class ProductSpecificationOut(ProductSpecificationCreate):
    id: int
    product_id: int
    bulk_order_id: Optional[int] = None

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    base_unit: str = "piece"
    standard_rate: float = 0.0
    images: Optional[str] = "[]"


class ProductOut(ProductCreate):
    id: int
    is_active: bool
    created_at: datetime
    specifications: Optional[List[ProductSpecificationOut]] = []

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float = 0.0
    specifications: Optional[str] = None


class OrderItemOut(OrderItemCreate):
    id: int
    bulk_order_id: int
    completed_quantity: int
    pending_quantity: int

    class Config:
        from_attributes = True


class BulkOrderCreate(BaseModel):
    title: str
    description: Optional[str] = None
    target_delivery_date: Optional[datetime] = None
    currency: str = "INR"
    notes: Optional[str] = None
    shg_id: Optional[int] = None
    items: List[OrderItemCreate] = []


class BulkOrderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_delivery_date: Optional[datetime] = None
    notes: Optional[str] = None
    shg_id: Optional[int] = None


class OrderStatusTransition(BaseModel):
    new_status: OrderStatus
    reason: Optional[str] = None


class BulkOrderOut(BaseModel):
    id: int
    order_number: str
    buyer_id: int
    shg_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: OrderStatus
    target_delivery_date: Optional[datetime] = None
    total_order_value: float
    approved_price_per_unit: float
    currency: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True
