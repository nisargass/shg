"""Structured States for LangGraph Agentic Workflows.

Maintains execution traces, intermediate artifacts, validation flags,
and agent execution logs while preventing unauthorized state mutations.
"""

from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class OrderPlanningState(TypedDict):
    # Inputs
    bulk_order_id: int
    order_item_id: int
    product_id: int
    total_quantity: int
    deadline: Optional[str]
    document_attachment: Optional[Dict[str, Any]]
    material_cost_estimate: Optional[float]
    labor_rate: Optional[float]
    target_margin_percentage: Optional[float]
    members: List[Dict[str, Any]]

    # Step outputs & state tracking
    is_order_valid: bool
    validation_errors: List[str]
    document_extraction: Optional[Dict[str, Any]]
    pricing_recommendation: Optional[Dict[str, Any]]
    capacity_analysis: Optional[Dict[str, Any]]
    completion_predictions: List[Dict[str, Any]]
    allocation_plan: Optional[Dict[str, Any]]
    inventory_check: Optional[Dict[str, Any]]
    execution_plan: Optional[Dict[str, Any]]
    risk_assessment: List[str]
    execution_log: List[Dict[str, Any]]
    requires_leader_approval: bool
    status: str  # PENDING_LEADER_APPROVAL, INFEASIBLE, VALIDATION_FAILED


class ProductionMonitoringState(TypedDict):
    # Inputs
    order_id: int
    target_quantity: int
    deadline: str
    start_date: Optional[str]
    member_updates: List[Dict[str, Any]]

    # Derived analysis
    elapsed_days: float
    remaining_days: float
    total_completed: int
    completion_percentage: float
    current_velocity_per_day: float
    required_velocity_per_day: float
    delay_risk_score: float
    risk_level: str  # LOW, MEDIUM, CRITICAL
    delayed_members: List[Dict[str, Any]]
    reallocation_recommendations: List[Dict[str, Any]]
    corrective_actions: List[str]
    execution_log: List[Dict[str, Any]]
    requires_leader_action: bool
    status: str


class QualityInspectionState(TypedDict):
    # Inputs
    batch_id: int
    product_id: int
    photo_urls: List[str]
    specifications: List[Dict[str, Any]]

    # Analysis
    image_quality_passed: bool
    image_quality_notes: str
    quality_score: float
    confidence_score: float
    detected_issues: List[str]
    deviations: List[Dict[str, Any]]
    inspection_report: Optional[Dict[str, Any]]
    suggested_action: str
    requires_human_review: bool
    execution_log: List[Dict[str, Any]]
