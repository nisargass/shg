from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.retail import RetailOrderStatus


class RetailOrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class RetailOrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True


class RetailOrderCreate(BaseModel):
    shipping_address: str
    items: List[RetailOrderItemCreate]


class RetailOrderOut(BaseModel):
    id: int
    order_number: str
    customer_id: int
    total_amount: float
    status: RetailOrderStatus
    shipping_address: str
    created_at: datetime
    items: List[RetailOrderItemOut] = []

    class Config:
        from_attributes = True
