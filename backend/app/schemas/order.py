from typing import Optional, List
from datetime import datetime, timezone
from pydantic import BaseModel, computed_field
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
    title: Optional[str] = "Bulk Wholesale Order"
    buyerName: Optional[str] = None
    productName: Optional[str] = None
    totalQuantity: Optional[int] = None
    unitAgreedPrice: Optional[float] = None
    deadline: Optional[str] = None
    specifications: Optional[str] = None
    category: Optional[str] = None
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

    @computed_field
    @property
    def buyerName(self) -> str:
        return "EcoFab Bangalore Retailers Ltd."

    @computed_field
    @property
    def productName(self) -> str:
        return self.title

    @computed_field
    @property
    def category(self) -> str:
        return "Garments & Textiles"

    @computed_field
    @property
    def totalQuantity(self) -> int:
        if self.items:
            return sum(it.quantity for it in self.items)
        return 500

    @computed_field
    @property
    def completedQuantity(self) -> int:
        if self.items:
            return sum(it.completed_quantity for it in self.items)
        return 0

    @computed_field
    @property
    def approvedQuantity(self) -> int:
        return self.completedQuantity

    @computed_field
    @property
    def reworkQuantity(self) -> int:
        return 0

    @computed_field
    @property
    def pendingQuantity(self) -> int:
        return max(0, self.totalQuantity - self.completedQuantity)

    @computed_field
    @property
    def unitAgreedPrice(self) -> float:
        return self.approved_price_per_unit if self.approved_price_per_unit > 0 else (self.items[0].unit_price if self.items else 165.0)

    @computed_field
    @property
    def orderDate(self) -> str:
        return self.created_at.strftime("%Y-%m-%d") if self.created_at else "2026-11-01"

    @computed_field
    @property
    def deadline(self) -> str:
        if self.target_delivery_date:
            return self.target_delivery_date.strftime("%Y-%m-%d")
        return "2026-11-20"

    @computed_field
    @property
    def daysRemaining(self) -> int:
        if self.target_delivery_date:
            delta = self.target_delivery_date.date() - datetime.now(timezone.utc).date()
            return max(0, delta.days)
        return 15

    @computed_field
    @property
    def allocationStatus(self) -> str:
        return "APPROVED" if self.status in [OrderStatus.IN_PRODUCTION, OrderStatus.COMPLETED] else "PENDING"

    @computed_field
    @property
    def qualityCheckStatus(self) -> str:
        return "IN_PROGRESS" if self.status == OrderStatus.IN_PRODUCTION else "NOT_STARTED"

    @computed_field
    @property
    def payoutStatus(self) -> str:
        return "AWAITING_FINAL_COMPLETION"

    @computed_field
    @property
    def specifications(self) -> str:
        return self.notes or ""

    @computed_field
    @property
    def poDocumentName(self) -> str:
        return f"PO_Order_{self.order_number}.pdf"

    @computed_field
    @property
    def assignedMembersCount(self) -> int:
        return 6

    class Config:
        from_attributes = True
