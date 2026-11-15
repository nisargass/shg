from typing import List, Optional
from pydantic import BaseModel, Field


class MonthlySales(BaseModel):
    month: str = Field(..., description="Month identifier, e.g. '2026-08' or 'Aug'")
    quantity: int = Field(..., ge=0, description="Units sold in this month")


class RetailDemandRequest(BaseModel):
    product_id: int
    historical_sales: List[MonthlySales] = Field(..., description="Chronological historical sales data")
    upcoming_festival_season: bool = Field(False, description="Whether festive surge (Diwali, Dasara) applies")
    product_category: Optional[str] = Field("Handloom", description="Product category for seasonal profile")
    lead_time_days: Optional[int] = Field(7, ge=1, description="Production or procurement lead time")


class RetailDemandResponse(BaseModel):
    success: bool = True
    product_id: int
    forecasted_monthly_demand: int = Field(..., description="Projected units for upcoming month")
    confidence_interval: List[int] = Field(..., description="[lower_bound, upper_bound] estimated range")
    confidence_score: float = Field(..., description="Confidence score 0.0 to 1.0")
    seasonal_factor: Optional[str] = Field(None, description="Applied seasonal multiplier explanation")
    explanation: str = Field(..., description="Assumptions and mathematical basis of forecast")
    forecast_period: str = Field("Next 30 Days", description="Timeframe over which demand is forecasted")
    factors: List[str] = Field(default_factory=list, description="Key factors influencing the demand trajectory")
    suggested_action: str = Field("MAINTAIN_STANDARD_REPLENISHMENT", description="Recommended operational action")
