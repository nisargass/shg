from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.work import AllocationStatus


class MemberAllocationProposal(BaseModel):
    member_id: int
    proposed_quantity: int
    completion_likelihood_percentage: float
    estimated_completion_date: Optional[datetime] = None
    confidence_score: float
    explanation: Optional[str] = None
    factors: Optional[List[str]] = []


class AIAllocationRecommendation(BaseModel):
    order_id: int
    order_item_id: int
    total_order_quantity: int
    recommendations: List[MemberAllocationProposal]
    unallocated_quantity: int
    notes: Optional[str] = None


class WorkAllocationCreate(BaseModel):
    bulk_order_id: int
    order_item_id: int
    member_id: int
    allocated_quantity: int = Field(..., gt=0)
    unit_rate: float = Field(..., ge=0.0)
    deadline: Optional[datetime] = None
    ai_recommended: bool = False
    ai_recommendation_id: Optional[str] = None


class WorkAllocationBatchCreate(BaseModel):
    bulk_order_id: int
    order_item_id: int
    allocations: List[WorkAllocationCreate]


class WorkAllocationUpdate(BaseModel):
    allocated_quantity: Optional[int] = None
    unit_rate: Optional[float] = None
    deadline: Optional[datetime] = None
    status: Optional[AllocationStatus] = None


class WorkAllocationOut(BaseModel):
    id: int
    bulk_order_id: int
    order_item_id: int
    member_id: int
    allocated_quantity: int
    completed_quantity: int
    unit_rate: float
    status: AllocationStatus
    assigned_at: datetime
    deadline: Optional[datetime] = None
    ai_recommended: bool
    ai_recommendation_id: Optional[str] = None
    progress_percentage: float

    class Config:
        from_attributes = True


class MemberTaskOut(BaseModel):
    id: int
    order_title: str
    order_number: str
    product_name: str
    allocated_quantity: int
    completed_quantity: int
    pending_quantity: int
    unit_rate: float
    deadline: Optional[datetime] = None
    status: AllocationStatus
    progress_percentage: float
