from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.exceptions import (
    AIException,
    ai_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
    http_exception_handler
)
from app.core.logging_config import setup_logging, logger
from app.schemas.common import HealthResponse
from app.api.v1.api import api_router
from app.api.v1.section14_router import section14_router
from app.rag.retriever import rag_retriever


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes application resources, logging, and RAG knowledge base."""
    setup_logging(debug=settings.DEBUG)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} ({settings.APP_ENV})")

    # Index knowledge base on startup
    try:
        num_chunks = rag_retriever.build_index()
        logger.info(f"Knowledge base indexed successfully: {num_chunks} document chunks ready.")
    except Exception as e:
        logger.warning(f"Could not build initial RAG index: {e}")

    yield

    logger.info("Shutting down AI Microservice.")


is_production = settings.APP_ENV.lower() in {"production", "prod"}

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Autonomous AI/ML Microservice for SHG Saathi. "
        "Provides 12 intelligent operational capabilities for Women's Self-Help Groups: "
        "OCR Document Intelligence, ML Workforce Completion Prediction, LP Work Allocation, "
        "CV Quality Inspection, Smart Pricing, Demand & Inventory Forecasting, Logistics, "
        "Financial Anomaly Detection (Isolation Forest), Multilingual RAG Assistant (Kannada, Hindi, English), "
        "Voice STT/TTS, and LangGraph Agentic Workflows."
    ),
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc",
    openapi_url=None if is_production else "/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom exception handlers
app.add_exception_handler(AIException, ai_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System Health"],
    summary="Microservice health and diagnostic check",
    description="Public status endpoint checking service uptime and provider readiness without requiring authentication."
)
@app.get(
    "/ai/v1/health",
    response_model=HealthResponse,
    tags=["System Health"],
    include_in_schema=False
)
def health_check() -> HealthResponse:
    """Returns service health, version, environment, and provider readiness."""
    providers_status = {
        "llm_provider": settings.LLM_PROVIDER,
        "vision_provider": settings.VISION_PROVIDER,
        "ocr_provider": settings.OCR_PROVIDER,
        "speech_provider": "whisper_configured" if settings.SPEECH_API_KEY else "unconfigured",
        "translation_provider": settings.TRANSLATION_PROVIDER,
        "rag_retriever": "ready" if rag_retriever._is_indexed else "indexing_pending",
        "ml_models": "loaded",
        "langgraph_agents": "ready"
    }

    return HealthResponse(
        service_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        status="healthy",
        environment=settings.APP_ENV,
        providers=providers_status
    )


# 1. Mount Section 14 contract specification endpoints directly under /ai/v1
app.include_router(section14_router, prefix="/ai/v1")

# 2. Mount full backend-compatible endpoints under /api/v1/ai
app.include_router(api_router, prefix="/api/v1/ai")
