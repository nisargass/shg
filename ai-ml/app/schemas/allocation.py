from typing import Any, List, Optional
from pydantic import BaseModel, Field


class AllocationMemberInput(BaseModel):
    member_id: int
    skills: List[str] = Field(default_factory=list)
    available_hours_per_day: float = Field(6.0, ge=0.5, le=24.0)
    current_workload: float = Field(0.0, ge=0.0)
    max_feasible_daily_quantity: float = Field(10.0, ge=0.1)
    historical_completion_rate: float = Field(95.0, ge=0.0, le=100.0)


class AllocationRequest(BaseModel):
    bulk_order_id: int
    order_item_id: int
    product_id: int
    total_quantity: int = Field(..., ge=1, description="Total units required for order item")
    deadline: Optional[str] = Field(None, description="ISO format order deadline")
    members: List[AllocationMemberInput] = Field(..., min_length=1, description="Candidate SHG members")


class MemberAllocationRecommendation(BaseModel):
    member_id: int
    proposed_quantity: int
    completion_likelihood_percentage: float
    estimated_completion_date: str
    confidence_score: float
    factors: List[str]
    explanation: str


class AllocationResponse(BaseModel):
    success: bool = True
    bulk_order_id: int
    order_item_id: int
    total_allocated: int
    unallocated_quantity: int
    recommendations: List[MemberAllocationRecommendation]
    fairness_index: float = Field(..., description="Fairness distribution index between 0.0 and 1.0")
    explanation: str

