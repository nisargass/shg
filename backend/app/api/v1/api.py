from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, shgs, members, orders, pricing, allocations,
    production, quality, inventory, earnings, payouts,
    retail, logistics, documents, assistant, notifications,
    suppliers, analytics, ai
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(shgs.router, prefix="/shgs", tags=["SHG Management"])
api_router.include_router(members.router, prefix="/members", tags=["Members & Capacity"])
api_router.include_router(orders.router, prefix="/orders", tags=["Bulk Orders & Products"])
api_router.include_router(pricing.router, prefix="/pricing", tags=["Pricing & Costing"])
api_router.include_router(allocations.router, prefix="/allocations", tags=["Work Allocation"])
api_router.include_router(production.router, prefix="/production", tags=["Production Tracking"])
api_router.include_router(quality.router, prefix="/quality", tags=["Quality Inspection"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory Management"])
api_router.include_router(earnings.router, prefix="/earnings", tags=["Member Earnings"])
api_router.include_router(payouts.router, prefix="/payouts", tags=["Group Payouts"])
api_router.include_router(retail.router, prefix="/retail", tags=["Retail Marketplace"])
api_router.include_router(logistics.router, prefix="/logistics", tags=["Logistics & Shipments"])
api_router.include_router(documents.router, prefix="/documents", tags=["Document OCR & Verification"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["Multilingual AI Assistant"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications & WebSocket"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Suppliers & Procurement"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics & Anomaly Audit"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI Audit Logs"])
