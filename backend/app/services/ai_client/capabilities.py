from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.services.ai_client.base_client import AIServiceClient
from app.services.ai_client.fallback_mock import FallbackAIMockService


class AICapabilitiesService:
    def __init__(self, client: Optional[AIServiceClient] = None):
        self.client = client or AIServiceClient()

    # 1. OCR Document Extraction
    def extract_document_ocr(
        self,
        document_id: int,
        document_type: str,
        file_url: str,
        mime_type: str,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        payload = {
            "document_id": document_id,
            "document_type": document_type,
            "file_url": file_url,
            "mime_type": mime_type
        }
        return self.client.post(
            endpoint="/api/v1/ai/ocr/extract",
            payload=payload,
            capability="OCR_DOCUMENT_EXTRACTION",
            ref_id=document_id,
            ref_type="Document",
            db=db,
            fallback_fn=lambda: FallbackAIMockService.mock_ocr(document_type, file_url)
        )

    # 2. Worker Completion Likelihood Prediction
    def predict_worker_completion_likelihood(
        self,
        member_id: int,
        product_id: int,
        proposed_quantity: int,
        deadline: Optional[str],
        available_hours_per_day: float,
        current_workload: float,
        historical_completion_rate: float,
        skills: List[str],
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        payload = {
            "member_id": member_id,
            "product_id": product_id,
            "proposed_quantity": proposed_quantity,
            "deadline": deadline,
            "available_hours_per_day": available_hours_per_day,
            "current_workload": current_workload,
            "historical_completion_rate": historical_completion_rate,
            "skills": skills
        }
        return self.client.post(
            endpoint="/api/v1/ai/workforce/completion-likelihood",
            payload=payload,
            capability="WORKER_COMPLETION_PREDICTION",
            ref_id=member_id,
            ref_type="SHGMember",
            db=db,
            fallback_fn=lambda: FallbackAIMockService.mock_worker_likelihood(
                member_id=member_id,
                proposed_qty=proposed_quantity,
                hours=available_hours_per_day,
                current_workload=current_workload,
                history_rate=historical_completion_rate
            )
        )

    # 3. Intelligent Work Allocation Recommendations
    def recommend_work_allocation(
        self,
        bulk_order_id: int,
        order_item_id: int,
        product_id: int,
        total_quantity: int,
        deadline: Optional[str],
        members: List[Dict[str, Any]],
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        payload = {
            "bulk_order_id": bulk_order_id,
            "order_item_id": order_item_id,
            "product_id": product_id,
            "total_quantity": total_quantity,
            "deadline": deadline,
            "members": members
        }
        return self.client.post(
            endpoint="/api/v1/ai/allocation/recommend",
            payload=payload,
            capability="WORK_ALLOCATION_RECOMMENDATION",
            ref_id=bulk_order_id,
            ref_type="BulkOrder",
            db=db,
            fallback_fn=lambda: FallbackAIMockService.mock_work_allocation(
                bulk_order_id=bulk_order_id,
                order_item_id=order_item_id,
                total_qty=total_quantity,
                members=members
            )
        )

    # 4. Computer Vision Quality Inspection
    def inspect_batch_quality(
        self,
        batch_id: int,
        product_id: int,
        photo_urls: List[str],
        specifications: List[Dict[str, Any]],
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        payload = {
            "batch_id": batch_id,
            "product_id": product_id,
            "photo_urls": photo_urls,
            "specifications": specifications
        }
        return self.client.post(
            endpoint="/api/v1/ai/quality/inspect-batch",
            payload=payload,
            capability="QUALITY_INSPECTION_CV",
            ref_id=batch_id,
            ref_type="ProductionBatch",
            db=db,
            fallback_fn=lambda: FallbackAIMockService.mock_quality_inspection(
                batch_id=batch_id,
                product_id=product_id,
                photo_urls=photo_urls
            )
        )

    # 5. Product Pricing Assistance
    def recommend_pricing(
        self,
        bulk_order_id: int,
        material_cost: float,
        labor_cost: float,
        packaging_cost: float,
        transport_cost: float,
        operational_expenses: float,
        quantity: int,
        target_margin_percentage: float = 15.0,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        payload = {
            "bulk_order_id": bulk_order_id,
            "material_cost": material_cost,
            "labor_cost": labor_cost,
            "packaging_cost": packaging_cost,
            "transport_cost": transport_cost,
            "operational_expenses": operational_expenses,
            "quantity": quantity,
            "target_margin_percentage": target_margin_percentage
        }
        return self.client.post(
            endpoint="/api/v1/ai/pricing/recommend",
            payload=payload,
            capability="PRICING_RECOMMENDATION",
            ref_id=bulk_order_id,
            ref_type="BulkOrder",
            db=db,
            fallback_fn=lambda: FallbackAIMockService.mock_pricing(
                material=material_cost,
                labor=labor_cost,
                packaging=packaging_cost,
                transport=transport_cost,
                ops=operational_expenses,
                qty=quantity,
                margin_pct=target_margin_percentage
            )
        )

    # 6. Retail Demand Forecasting
    def forecast_retail_demand(
        self,
        product_id: int,
        historical_sales: List[Dict[str, Any]],
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        payload = {
            "product_id": product_id,
            "historical_sales": historical_sales
        }
        return self.client.post(
            endpoint="/api/v1/ai/retail/forecast-demand",
            payload=payload,
            capability="RETAIL_DEMAND_FORECAST",
            ref_id=product_id,
            ref_type="Product",
            db=db,
            fallback_fn=lambda: {
                "success": True,
                "product_id": product_id,
                "forecasted_monthly_demand": 50,
                "confidence_score": 0.80,
                "is_fallback": True
            }
        )

    # 7. Inventory Forecasting
    def forecast_inventory_restock(
        self,
        shg_id: int,
        inventory_id: int,
        current_stock: float,
        lead_time_days: int = 7,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        payload = {
            "shg_id": shg_id,
            "inventory_id": inventory_id,
            "current_physical_stock": current_stock,
            "lead_time_days": lead_time_days
        }
        return self.client.post(
            endpoint="/api/v1/ai/inventory/forecast-restock",
            payload=payload,
            capability="INVENTORY_RESTOCK_FORECAST",
            ref_id=inventory_id,
            ref_type="Inventory",
            db=db,
            fallback_fn=lambda: {
                "success": True,
                "inventory_id": inventory_id,
                "days_until_stockout": 5.0,
                "restock_recommended": current_stock < 15.0,
                "recommended_order_quantity": 50.0,
                "is_fallback": True
            }
        )

    # 8. Logistics Recommendations
    def recommend_logistics(
        self,
        origin: str,
        destination: str,
        weight_kg: float,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        payload = {
            "origin": origin,
            "destination": destination,
            "weight_kg": weight_kg
        }
        return self.client.post(
            endpoint="/api/v1/ai/logistics/recommend-route",
            payload=payload,
            capability="LOGISTICS_RECOMMENDATION",
            db=db,
            fallback_fn=lambda: {
                "success": True,
                "recommended_carriers": [{"carrier_name": "Standard Regional Parcel Carrier", "estimated_transit_hours": 24}],
                "is_fallback": True
            }
        )

    # 9. Financial Anomaly Detection
    def detect_financial_anomalies(
        self,
        shg_id: int,
        earnings_records: List[Dict[str, Any]],
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        payload = {
            "shg_id": shg_id,
            "earnings_records": earnings_records
        }
        return self.client.post(
            endpoint="/api/v1/ai/finance/detect-anomalies",
            payload=payload,
            capability="FINANCIAL_ANOMALY_DETECTION",
            ref_id=shg_id,
            ref_type="SHG",
            db=db,
            fallback_fn=lambda: FallbackAIMockService.mock_financial_anomalies(earnings_records)
        )

    # 10. RAG Knowledge Assistant
    def query_rag_assistant(
        self,
        query: str,
        language: str = "en",
        user_context: Optional[Dict[str, Any]] = None,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        payload = {
            "query": query,
            "language": language,
            "user_context": user_context or {}
        }
        return self.client.post(
            endpoint="/api/v1/ai/assistant/query",
            payload=payload,
            capability="RAG_KNOWLEDGE_ASSISTANT",
            db=db,
            fallback_fn=lambda: FallbackAIMockService.mock_rag_assistant(query, language)
        )

    # 11. Speech-to-Text & Text-to-Speech
    def speech_to_text(self, audio_bytes_base64: str, language: str = "kn", db: Optional[Session] = None) -> Dict[str, Any]:
        payload = {"audio_base64": audio_bytes_base64, "language": language}
        return self.client.post(
            endpoint="/api/v1/ai/voice/stt",
            payload=payload,
            capability="VOICE_SPEECH_TO_TEXT",
            db=db,
            fallback_fn=lambda: {"text": "Voice input received.", "language": language, "is_fallback": True}
        )

    # 12. Multilingual Response Generation / Translation
    def translate_message(self, text: str, target_languages: List[str], db: Optional[Session] = None) -> Dict[str, Any]:
        payload = {"text": text, "target_languages": target_languages}
        return self.client.post(
            endpoint="/api/v1/ai/translate",
            payload=payload,
            capability="MULTILINGUAL_TRANSLATION",
            db=db,
            fallback_fn=lambda: {"translations": {lang: text for lang in target_languages}, "is_fallback": True}
        )


ai_service_client = AICapabilitiesService()
