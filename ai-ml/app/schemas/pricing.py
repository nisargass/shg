from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


class MarketBenchmarkRange(BaseModel):
    min_unit_price: float
    max_unit_price: float
    source: Optional[str] = "Regional SHG Market Benchmark"


class PricingRequest(BaseModel):
    bulk_order_id: Optional[int] = Field(1, description="Bulk order ID if applicable")
    product_type: Optional[str] = Field("Handloom / Handicraft", description="Product category")
    material_cost: float = Field(..., ge=0.0, description="Total raw material expenses in INR")
    labor_cost: float = Field(..., ge=0.0, description="Total artisan labor compensation in INR")
    packaging_cost: float = Field(0.0, ge=0.0, description="Packaging materials expense in INR")
    transport_cost: float = Field(0.0, ge=0.0, description="Freight and transit expense in INR")
    operational_expenses: float = Field(0.0, ge=0.0, description="Electricity, machine wear, utilities")
    quantity: int = Field(..., ge=1, description="Total units in bulk order")
    target_margin_percentage: float = Field(15.0, ge=0.0, lt=100.0, description="Target profit margin % (must be < 100%)")


class PricingResponse(BaseModel):
    success: bool = True
    recommended_selling_price_per_unit: float = Field(..., description="Suggested selling price per unit")
    recommended_unit_price: Optional[float] = Field(None, description="Alias for recommended_selling_price_per_unit")
    recommended_total_order_value: float = Field(..., description="Total bulk order value in INR")
    estimated_profit: float = Field(..., description="Estimated net profit in INR")
    margin_percentage: float = Field(..., description="Actual profit margin achieved")
    missing_cost_warnings: List[str] = Field(default_factory=list, description="Warnings for omitted overheads")
    market_benchmark_range: Optional[MarketBenchmarkRange] = None

    @model_validator(mode="after")
    def populate_alias(self):
        if self.recommended_unit_price is None:
            self.recommended_unit_price = self.recommended_selling_price_per_unit
        return self
