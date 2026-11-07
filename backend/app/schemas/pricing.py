from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PricingBreakdownCreate(BaseModel):
    bulk_order_id: int
    total_material_cost: float = Field(..., ge=0.0, description="Material cost")
    labor_cost: float = Field(..., ge=0.0, description="Labor cost")
    packaging_cost: float = Field(..., ge=0.0, description="Packaging cost")
    transportation_cost: float = Field(..., ge=0.0, description="Transportation cost")
    operational_expenses: float = Field(..., ge=0.0, description="Other operational expenses")
    profit_margin_percentage: float = Field(15.0, ge=0.0, description="Desired profit margin percentage")
    notes: Optional[str] = None


class PricingApprovalRequest(BaseModel):
    is_approved: bool
    final_approved_price: Optional[float] = None
    notes: Optional[str] = None


class PricingBreakdownOut(BaseModel):
    id: int
    bulk_order_id: int
    total_material_cost: float
    labor_cost: float
    packaging_cost: float
    transportation_cost: float
    operational_expenses: float
    profit_margin_percentage: float
    calculated_unit_price: float
    suggested_selling_price: float
    final_approved_price: Optional[float] = None
    is_approved: bool
    approved_by_id: Optional[int] = None
    approved_at: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    total_cost: float

    class Config:
        from_attributes = True
