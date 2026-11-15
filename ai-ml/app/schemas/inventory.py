from typing import Optional, List
from pydantic import BaseModel, Field


class InventoryRestockRequest(BaseModel):
    shg_id: int
    inventory_id: int
    current_physical_stock: float = Field(..., ge=0.0, description="Total physical inventory in storage")
    bulk_committed_stock: float = Field(0.0, ge=0.0, description="Stock reserved for confirmed bulk orders")
    retail_reserved_stock: Optional[float] = Field(0.0, ge=0.0, description="Stock reserved for direct retail orders")
    lead_time_days: int = Field(7, ge=1, description="Supplier delivery lead time in days")
    daily_burn_rate: Optional[float] = Field(None, ge=0.0, description="Average daily consumption in units/day")


class InventoryRestockResponse(BaseModel):
    success: bool = True
    inventory_id: int
    physical_stock: float = Field(..., description="Total units physically in storage")
    bulk_reserved_stock: float = Field(0.0, description="Units locked for bulk order fulfillment")
    retail_reserved_stock: float = Field(0.0, description="Units locked for retail shelf orders")
    free_stock: float = Field(..., description="Uncommitted units available for new orders")
    days_until_stockout: float = Field(..., description="Estimated days before usable stock drops to 0")
    restock_recommended: bool = Field(..., description="Whether a replenishment PO should be raised")
    recommended_order_quantity: float = Field(..., description="Calculated reorder quantity")
    urgency: str = Field(..., description="CRITICAL, HIGH, MEDIUM, LOW")
    suggested_action: str = Field("ORDER_RAW_MATERIALS", description="Actionable inventory guidance")
    explanation: str = Field(..., description="Stock buffer breakdown and formula explanation")
