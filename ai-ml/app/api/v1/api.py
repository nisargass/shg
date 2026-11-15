from fastapi import APIRouter
from app.api.v1.endpoints import (
    ocr,
    workforce,
    allocation,
    quality,
    pricing,
    retail,
    inventory,
    logistics,
    finance,
    assistant,
    voice,
    translation,
    agents
)

api_router = APIRouter()

api_router.include_router(ocr.router, tags=["OCR & Document Extraction"])
api_router.include_router(workforce.router, tags=["Workforce Analytics"])
api_router.include_router(allocation.router, tags=["Work Allocation"])
api_router.include_router(quality.router, tags=["Quality Inspection (CV)"])
api_router.include_router(pricing.router, tags=["Product Pricing"])
api_router.include_router(retail.router, tags=["Retail Demand Forecasting"])
api_router.include_router(inventory.router, tags=["Inventory Restock"])
api_router.include_router(logistics.router, tags=["Logistics & Delivery"])
api_router.include_router(finance.router, tags=["Financial Anomaly Detection"])
api_router.include_router(assistant.router, tags=["RAG Multilingual Assistant"])
api_router.include_router(voice.router, tags=["Speech Processing (STT / TTS)"])
api_router.include_router(translation.router, tags=["Multilingual Translation"])
api_router.include_router(agents.router, tags=["LangGraph Multi-Agent Workflows"])
