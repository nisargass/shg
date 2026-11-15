"""Pydantic Request and Response Schemas for LangGraph Agentic Workflows."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.schemas.allocation import AllocationMemberInput


class OrderPlanningAgentRequest(BaseModel):
    bulk_order_id: int
    order_item_id: int
    product_id: int
    total_quantity: int = Field(..., ge=1, description="Total units required for order")
    deadline: Optional[str] = Field(None, description="Order delivery deadline (ISO format)")
    document_attachment: Optional[Dict[str, Any]] = Field(None, description="Optional uploaded PO or specification document metadata")
    material_cost_estimate: Optional[float] = Field(None, ge=0.0)
    labor_rate: Optional[float] = Field(None, ge=0.0)
    target_margin_percentage: Optional[float] = Field(20.0, ge=0.0, lt=100.0)
    members: List[AllocationMemberInput] = Field(..., min_length=1, description="Candidate SHG members")


class OrderPlanningAgentResponse(BaseModel):
    success: bool = True
    status: str
    bulk_order_id: int
    total_quantity: int
    requires_leader_approval: bool = True
    execution_plan: Optional[Dict[str, Any]] = None
    pricing_recommendation: Optional[Dict[str, Any]] = None
    allocation_plan: Optional[Dict[str, Any]] = None
    inventory_check: Optional[Dict[str, Any]] = None
    risk_assessment: List[str] = []
    execution_log: List[Dict[str, Any]] = []


class MemberProgressUpdate(BaseModel):
    member_id: int
    assigned_quantity: int = Field(..., ge=1)
    completed_quantity: int = Field(..., ge=0)
    expected_quantity_to_date: Optional[int] = None
    notes: Optional[str] = None


class ProductionMonitoringAgentRequest(BaseModel):
    order_id: int
    target_quantity: int = Field(..., ge=1)
    deadline: str
    start_date: Optional[str] = None
    member_updates: List[MemberProgressUpdate] = Field(default_factory=list)


class ProductionMonitoringAgentResponse(BaseModel):
    success: bool = True
    order_id: int
    status: str
    total_completed: int
    completion_percentage: float
    delay_risk_score: float
    risk_level: str
    delayed_members: List[Dict[str, Any]] = []
    reallocation_recommendations: List[Dict[str, Any]] = []
    corrective_actions: List[str] = []
    requires_leader_action: bool
    execution_log: List[Dict[str, Any]] = []


class QualityInspectionAgentRequest(BaseModel):
    batch_id: int
    product_id: int
    photo_urls: List[str] = Field(..., min_length=1)
    specifications: List[Dict[str, Any]] = Field(default_factory=list)


class QualityInspectionAgentResponse(BaseModel):
    success: bool = True
    batch_id: int
    quality_score: float
    confidence_score: float
    suggested_action: str
    requires_human_review: bool = True
    detected_issues: List[str] = []
    inspection_report: Optional[Dict[str, Any]] = None
    execution_log: List[Dict[str, Any]] = []
