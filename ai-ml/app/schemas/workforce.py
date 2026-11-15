from typing import List, Optional
from pydantic import BaseModel, Field


class WorkforceLikelihoodRequest(BaseModel):
    member_id: int = Field(..., description="Unique ID of SHG member")
    product_id: int = Field(..., description="ID of product being manufactured")
    proposed_quantity: int = Field(..., ge=1, description="Quantity proposed to allocate to member")
    deadline: Optional[str] = Field(None, description="ISO format deadline timestamp")
    available_hours_per_day: float = Field(..., ge=0.5, le=24.0, description="Daily working hours available")
    current_workload: float = Field(0.0, ge=0.0, description="Active backlog of units already assigned")
    historical_completion_rate: float = Field(100.0, ge=0.0, le=100.0, description="Past completion rate %")
    skills: List[str] = Field(default_factory=list, description="List of craft/manufacturing skills")


class WorkforceLikelihoodResponse(BaseModel):
    success: bool = True
    member_id: int
    completion_likelihood_percentage: float = Field(..., description="Calculated likelihood 0-100%")
    estimated_completion_date: str = Field(..., description="Estimated completion date (ISO format)")
    confidence_score: float = Field(..., description="Model confidence 0.0-1.0")
    factors: List[str] = Field(..., description="Key driving factors influencing prediction")
    explanation: str = Field(..., description="Human-understandable summary of prediction")

