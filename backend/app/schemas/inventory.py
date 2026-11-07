from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.inventory import InventoryItemType, ReservationStatus, PurchaseStatus


class InventoryCreate(BaseModel):
    shg_id: int
    item_type: InventoryItemType = InventoryItemType.RAW_MATERIAL
    item_name: str
    unit: str = "kg"
    physical_stock: float = Field(0.0, ge=0.0)
    unit_cost: float = Field(0.0, ge=0.0)
    low_stock_threshold: float = Field(10.0, ge=0.0)


class InventoryUpdate(BaseModel):
    physical_stock: Optional[float] = None
    damaged_stock: Optional[float] = None
    unit_cost: Optional[float] = None
    low_stock_threshold: Optional[float] = None


class InventoryStockAdjust(BaseModel):
    quantity_delta: float
    reason: str


class InventoryOut(BaseModel):
    id: int
    shg_id: int
    item_type: InventoryItemType
    item_name: str
    unit: str
    physical_stock: float
    bulk_reserved_stock: float
    retail_reserved_stock: float
    damaged_stock: float
    unit_cost: float
    low_stock_threshold: float
    available_stock: float
    updated_at: datetime

    class Config:
        from_attributes = True


class ReservationCreate(BaseModel):
    inventory_id: int
    order_type: str = Field(..., description="BULK or RETAIL")
    order_id: int
    reserved_quantity: float = Field(..., gt=0.0)


class ReservationOut(BaseModel):
    id: int
    inventory_id: int
    order_type: str
    order_id: int
    reserved_quantity: float
    status: ReservationStatus
    created_at: datetime

    class Config:
        from_attributes = True


class SupplierCreate(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    materials_supplied: Optional[List[str]] = []


class SupplierOut(BaseModel):
    id: int
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    materials_supplied: Optional[str] = "[]"
    reliability_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class MaterialPurchaseCreate(BaseModel):
    shg_id: int
    supplier_id: int
    material_name: str
    quantity: float = Field(..., gt=0.0)
    unit: str = "kg"
    unit_price: float = Field(..., ge=0.0)
    shortage_or_damage_notes: Optional[str] = None


class MaterialPurchaseReceive(BaseModel):
    received_quantity: float = Field(..., ge=0.0)
    shortage_or_damage_notes: Optional[str] = None


class MaterialPurchaseOut(BaseModel):
    id: int
    shg_id: int
    supplier_id: int
    material_name: str
    quantity: float
    unit: str
    unit_price: float
    total_cost: float
    purchase_date: datetime
    status: PurchaseStatus
    received_date: Optional[datetime] = None
    shortage_or_damage_notes: Optional[str] = None
    invoice_document_id: Optional[int] = None

    class Config:
        from_attributes = True
