"""Section 14 API Contract Specification Router.

Directly implements all endpoints specified in Section 14 of the Master Prompt:
- POST /ai/v1/documents/extract
- POST /ai/v1/allocation/predict
- POST /ai/v1/allocation/recommend
- POST /ai/v1/quality/inspect
- POST /ai/v1/pricing/recommend
- POST /ai/v1/inventory/forecast
- POST /ai/v1/retail/demand-forecast
- POST /ai/v1/logistics/recommend
- POST /ai/v1/finance/anomaly-detect
- POST /ai/v1/assistant/chat
- POST /ai/v1/assistant/speech-to-text
- POST /ai/v1/assistant/text-to-speech
- POST /ai/v1/agents/order-planning
- POST /ai/v1/agents/production-monitoring
"""

from fastapi import APIRouter
from app.schemas.ocr import OCRRequest, OCRResponse
from app.schemas.workforce import WorkforceLikelihoodRequest, WorkforceLikelihoodResponse
from app.schemas.allocation import AllocationRequest, AllocationResponse
from app.schemas.quality import QualityInspectionRequest, QualityInspectionResponse
from app.schemas.pricing import PricingRequest, PricingResponse
from app.schemas.inventory import InventoryRestockRequest, InventoryRestockResponse
from app.schemas.retail import RetailDemandRequest, RetailDemandResponse
from app.schemas.logistics import LogisticsRequest, LogisticsResponse
from app.schemas.finance import FinancialAnomalyRequest, FinancialAnomalyResponse
from app.schemas.assistant import AssistantQueryRequest, AssistantQueryResponse
from app.schemas.voice import STTRequest, STTResponse, TTSRequest, TTSResponse
from app.schemas.agents import (
    OrderPlanningAgentRequest,
    OrderPlanningAgentResponse,
    ProductionMonitoringAgentRequest,
    ProductionMonitoringAgentResponse
)

from app.services.ocr_service import ocr_service
from app.services.workforce_service import workforce_service
from app.services.allocation_service import allocation_service
from app.services.quality_service import quality_service
from app.services.pricing_service import pricing_service
from app.services.inventory_service import inventory_service
from app.services.retail_service import retail_service
from app.services.logistics_service import logistics_service
from app.services.finance_service import finance_service
from app.services.assistant_service import assistant_service
from app.services.voice_service import voice_service
from app.services.agents.order_planning_graph import order_planning_graph
from app.services.agents.production_monitoring_graph import production_monitoring_graph

section14_router = APIRouter()


@section14_router.post("/documents/extract", response_model=OCRResponse, tags=["Master Prompt Section 14"])
def extract_documents(req: OCRRequest) -> OCRResponse:
    return ocr_service.extract_document(req)


@section14_router.post("/allocation/predict", response_model=WorkforceLikelihoodResponse, tags=["Master Prompt Section 14"])
def predict_completion(req: WorkforceLikelihoodRequest) -> WorkforceLikelihoodResponse:
    return workforce_service.predict_completion_likelihood(req)


@section14_router.post("/allocation/recommend", response_model=AllocationResponse, tags=["Master Prompt Section 14"])
def recommend_allocation(req: AllocationRequest) -> AllocationResponse:
    return allocation_service.recommend_allocation(req)


@section14_router.post("/quality/inspect", response_model=QualityInspectionResponse, tags=["Master Prompt Section 14"])
def inspect_quality(req: QualityInspectionRequest) -> QualityInspectionResponse:
    return quality_service.inspect_batch(req)


@section14_router.post("/pricing/recommend", response_model=PricingResponse, tags=["Master Prompt Section 14"])
def recommend_pricing(req: PricingRequest) -> PricingResponse:
    return pricing_service.recommend_pricing(req)


@section14_router.post("/inventory/forecast", response_model=InventoryRestockResponse, tags=["Master Prompt Section 14"])
def forecast_inventory(req: InventoryRestockRequest) -> InventoryRestockResponse:
    return inventory_service.forecast_restock(req)


@section14_router.post("/retail/demand-forecast", response_model=RetailDemandResponse, tags=["Master Prompt Section 14"])
def forecast_retail_demand(req: RetailDemandRequest) -> RetailDemandResponse:
    return retail_service.forecast_demand(req)


@section14_router.post("/logistics/recommend", response_model=LogisticsResponse, tags=["Master Prompt Section 14"])
def recommend_logistics(req: LogisticsRequest) -> LogisticsResponse:
    return logistics_service.recommend_route(req)


@section14_router.post("/finance/anomaly-detect", response_model=FinancialAnomalyResponse, tags=["Master Prompt Section 14"])
def detect_financial_anomalies(req: FinancialAnomalyRequest) -> FinancialAnomalyResponse:
    return finance_service.detect_anomalies(req)


@section14_router.post("/assistant/chat", response_model=AssistantQueryResponse, tags=["Master Prompt Section 14"])
def chat_assistant(req: AssistantQueryRequest) -> AssistantQueryResponse:
    return assistant_service.answer_query(req)


@section14_router.post("/assistant/speech-to-text", response_model=STTResponse, tags=["Master Prompt Section 14"])
def assistant_stt(req: STTRequest) -> STTResponse:
    return voice_service.process_stt(audio_base64=req.audio_base64, language=req.language)


@section14_router.post("/assistant/text-to-speech", response_model=TTSResponse, tags=["Master Prompt Section 14"])
def assistant_tts(req: TTSRequest) -> TTSResponse:
    return voice_service.process_tts(req)


@section14_router.post("/agents/order-planning", response_model=OrderPlanningAgentResponse, tags=["Master Prompt Section 14"])
def agents_order_planning(req: OrderPlanningAgentRequest) -> OrderPlanningAgentResponse:
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


@section14_router.post("/agents/production-monitoring", response_model=ProductionMonitoringAgentResponse, tags=["Master Prompt Section 14"])
def agents_production_monitoring(req: ProductionMonitoringAgentRequest) -> ProductionMonitoringAgentResponse:
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
