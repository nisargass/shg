# Export all schemas
from app.schemas.common import APIResponse, ErrorResponse, HealthResponse
from app.schemas.ocr import OCRRequest, OCRResponse
from app.schemas.workforce import WorkforceLikelihoodRequest, WorkforceLikelihoodResponse
from app.schemas.allocation import AllocationRequest, AllocationResponse
from app.schemas.quality import QualityInspectionRequest, QualityInspectionResponse
from app.schemas.pricing import PricingRequest, PricingResponse
from app.schemas.retail import RetailDemandRequest, RetailDemandResponse
from app.schemas.inventory import InventoryRestockRequest, InventoryRestockResponse
from app.schemas.logistics import LogisticsRequest, LogisticsResponse
from app.schemas.finance import FinancialAnomalyRequest, FinancialAnomalyResponse
from app.schemas.assistant import AssistantQueryRequest, AssistantQueryResponse
from app.schemas.voice import STTRequest, STTResponse, TTSRequest, TTSResponse
from app.schemas.translation import TranslationRequest, TranslationResponse

__all__ = [
    "APIResponse",
    "ErrorResponse",
    "HealthResponse",
    "OCRRequest",
    "OCRResponse",
    "WorkforceLikelihoodRequest",
    "WorkforceLikelihoodResponse",
    "AllocationRequest",
    "AllocationResponse",
    "QualityInspectionRequest",
    "QualityInspectionResponse",
    "PricingRequest",
    "PricingResponse",
    "RetailDemandRequest",
    "RetailDemandResponse",
    "InventoryRestockRequest",
    "InventoryRestockResponse",
    "LogisticsRequest",
    "LogisticsResponse",
    "FinancialAnomalyRequest",
    "FinancialAnomalyResponse",
    "AssistantQueryRequest",
    "AssistantQueryResponse",
    "STTRequest",
    "STTResponse",
    "TTSRequest",
    "TTSResponse",
    "TranslationRequest",
    "TranslationResponse",
]

