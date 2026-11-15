"""FastAPI Endpoints for LangGraph Multi-Agent Workflows."""

from fastapi import APIRouter, HTTPException, status
from app.schemas.agents import (
    OrderPlanningAgentRequest,
    OrderPlanningAgentResponse,
    ProductionMonitoringAgentRequest,
    ProductionMonitoringAgentResponse,
    QualityInspectionAgentRequest,
    QualityInspectionAgentResponse
)
from app.services.agents.order_planning_graph import order_planning_graph
from app.services.agents.production_monitoring_graph import production_monitoring_graph
from app.services.agents.quality_inspection_graph import quality_inspection_graph

router = APIRouter(prefix="/agents", tags=["LangGraph Multi-Agent Workflows"])


@router.post(
    "/order-planning",
    response_model=OrderPlanningAgentResponse,
    summary="Multi-Agent Bulk Order Planning Workflow",
    description=(
        "Executes 7-node LangGraph agentic workflow: validates order, extracts document metadata (OCR), "
        "evaluates smart pricing, runs ML completion prediction, optimizes work distribution via Linear Programming, "
        "checks inventory raw materials, and synthesizes an execution plan. "
        "Strictly requires SHG leader approval before database persistence."
    )
)
def plan_bulk_order(req: OrderPlanningAgentRequest) -> OrderPlanningAgentResponse:
    initial_state = {
        "bulk_order_id": req.bulk_order_id,
        "order_item_id": req.order_item_id,
        "product_id": req.product_id,
        "total_quantity": req.total_quantity,
        "deadline": req.deadline,
        "document_attachment": req.document_attachment,
        "material_cost_estimate": req.material_cost_estimate,
        "labor_rate": req.labor_rate,
        "target_margin_percentage": req.target_margin_percentage,
        "members": [m.model_dump() for m in req.members],
        "is_order_valid": True,
        "validation_errors": [],
        "document_extraction": None,
        "pricing_recommendation": None,
        "capacity_analysis": None,
        "completion_predictions": [],
        "allocation_plan": None,
        "inventory_check": None,
        "execution_plan": None,
        "risk_assessment": [],
        "execution_log": [],
        "requires_leader_approval": True,
        "status": "PROCESSING"
    }

    final_state = order_planning_graph.invoke(initial_state)

    return OrderPlanningAgentResponse(
        success=final_state.get("status") != "VALIDATION_FAILED",
        status=final_state.get("status", "COMPLETED"),
        bulk_order_id=req.bulk_order_id,
        total_quantity=req.total_quantity,
        requires_leader_approval=True,
        execution_plan=final_state.get("execution_plan"),
        pricing_recommendation=final_state.get("pricing_recommendation"),
        allocation_plan=final_state.get("allocation_plan"),
        inventory_check=final_state.get("inventory_check"),
        risk_assessment=final_state.get("risk_assessment", []),
        execution_log=final_state.get("execution_log", [])
    )


@router.post(
    "/production-monitoring",
    response_model=ProductionMonitoringAgentResponse,
    summary="Multi-Agent Production Monitoring & Delay Prediction Workflow",
    description=(
        "Executes 4-node LangGraph agentic workflow: tracks artisan completion velocity, computes delay risk scores, "
        "proposes workload rebalancing from lagging artisans to available capacity, and formats alert for SHG leader."
    )
)
def monitor_production(req: ProductionMonitoringAgentRequest) -> ProductionMonitoringAgentResponse:
    initial_state = {
        "order_id": req.order_id,
        "target_quantity": req.target_quantity,
        "deadline": req.deadline,
        "start_date": req.start_date,
        "member_updates": [u.model_dump() for u in req.member_updates],
        "elapsed_days": 0.0,
        "remaining_days": 0.0,
        "total_completed": 0,
        "completion_percentage": 0.0,
        "current_velocity_per_day": 0.0,
        "required_velocity_per_day": 0.0,
        "delay_risk_score": 0.0,
        "risk_level": "LOW",
        "delayed_members": [],
        "reallocation_recommendations": [],
        "corrective_actions": [],
        "execution_log": [],
        "requires_leader_action": False,
        "status": "PROCESSING"
    }

    final_state = production_monitoring_graph.invoke(initial_state)

    return ProductionMonitoringAgentResponse(
        success=True,
        order_id=req.order_id,
        status=final_state.get("status", "COMPLETED"),
        total_completed=final_state.get("total_completed", 0),
        completion_percentage=final_state.get("completion_percentage", 0.0),
        delay_risk_score=final_state.get("delay_risk_score", 0.0),
        risk_level=final_state.get("risk_level", "LOW"),
        delayed_members=final_state.get("delayed_members", []),
        reallocation_recommendations=final_state.get("reallocation_recommendations", []),
        corrective_actions=final_state.get("corrective_actions", []),
        requires_leader_action=final_state.get("requires_leader_action", False),
        execution_log=final_state.get("execution_log", [])
    )


@router.post(
    "/quality-inspection",
    response_model=QualityInspectionAgentResponse,
    summary="Multi-Agent Quality Inspection Workflow",
    description=(
        "Executes 3-node LangGraph workflow: gates image quality (blur, lighting, resolution), "
        "evaluates computer vision manufacturing specifications, and formats inspection report for human reviewer."
    )
)
def inspect_quality_agent(req: QualityInspectionAgentRequest) -> QualityInspectionAgentResponse:
    initial_state = {
        "batch_id": req.batch_id,
        "product_id": req.product_id,
        "photo_urls": req.photo_urls,
        "specifications": req.specifications,
        "image_quality_passed": True,
        "image_quality_notes": "",
        "quality_score": 0.0,
        "confidence_score": 0.0,
        "detected_issues": [],
        "deviations": [],
        "inspection_report": None,
        "suggested_action": "HUMAN_REVIEW",
        "requires_human_review": True,
        "execution_log": []
    }

    final_state = quality_inspection_graph.invoke(initial_state)

    return QualityInspectionAgentResponse(
        success=True,
        batch_id=req.batch_id,
        quality_score=final_state.get("quality_score", 85.0),
        confidence_score=final_state.get("confidence_score", 0.88),
        suggested_action=final_state.get("suggested_action", "HUMAN_REVIEW"),
        requires_human_review=True,
        detected_issues=final_state.get("detected_issues", []),
        inspection_report=final_state.get("inspection_report"),
        execution_log=final_state.get("execution_log", [])
    )
