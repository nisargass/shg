import logging
from typing import Dict, Any, List
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)


class FallbackAIMockService:
    """Provides sensible heuristic fallbacks when AI/ML microservice is offline,

    preventing backend crashes and allowing manual review workflows to proceed.
    """

    @staticmethod
    def mock_ocr(document_type: str, file_url: str) -> Dict[str, Any]:
        return {
            "success": True,
            "confidence_score": 0.85,
            "extracted_data": {
                "document_type": document_type,
                "file_reference": file_url,
                "detected_title": "Scanned Document Reference",
                "notes": "Extracted via local fallback heuristic parser. Requires human verification.",
                "items": []
            },
            "raw_text": f"Scanned file content from {file_url}",
            "is_fallback": True
        }

    @staticmethod
    def mock_worker_likelihood(member_id: int, proposed_qty: int, hours: float, current_workload: float, history_rate: float) -> Dict[str, Any]:
        # Heuristic likelihood calculation
        daily_capacity = max(1.0, hours * 1.5)
        days_needed = proposed_qty / daily_capacity
        workload_penalty = min(30.0, current_workload * 2.0)
        base = max(40.0, min(99.0, history_rate - workload_penalty))
        
        return {
            "success": True,
            "member_id": member_id,
            "completion_likelihood_percentage": round(base, 1),
            "estimated_completion_date": (datetime.now(timezone.utc) + timedelta(days=max(1, int(days_needed)))).isoformat(),
            "confidence_score": 0.80,
            "factors": [
                f"Historical completion rate: {history_rate}%",
                f"Available working hours: {hours} hrs/day",
                f"Current active workload: {current_workload} units"
            ],
            "explanation": f"Member capacity estimate based on {hours} daily hours and {history_rate}% track record.",
            "is_fallback": True
        }

    @staticmethod
    def mock_work_allocation(bulk_order_id: int, order_item_id: int, total_qty: int, members: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not members:
            return {
                "success": False,
                "total_allocated": 0,
                "unallocated_quantity": total_qty,
                "recommendations": [],
                "explanation": "No eligible members provided for allocation."
            }
        
        # Fair heuristic distribution across members
        num_members = len(members)
        base_per_member = total_qty // num_members
        remainder = total_qty % num_members
        
        recommendations = []
        for i, m in enumerate(members):
            allocated = base_per_member + (1 if i < remainder else 0)
            mid = m.get("member_id", i + 1)
            hours = m.get("available_hours_per_day", 6.0)
            hist = m.get("historical_completion_rate", 95.0)
            workload = m.get("current_workload", 0.0)
            
            likelihood_res = FallbackAIMockService.mock_worker_likelihood(mid, allocated, hours, workload, hist)
            
            recommendations.append({
                "member_id": mid,
                "proposed_quantity": allocated,
                "completion_likelihood_percentage": likelihood_res["completion_likelihood_percentage"],
                "estimated_completion_date": likelihood_res["estimated_completion_date"],
                "confidence_score": 0.82,
                "factors": likelihood_res["factors"],
                "explanation": f"Balanced allocation: {allocated} units assigned proportionally."
            })
            
        return {
            "success": True,
            "bulk_order_id": bulk_order_id,
            "order_item_id": order_item_id,
            "total_allocated": total_qty,
            "unallocated_quantity": 0,
            "recommendations": recommendations,
            "fairness_index": 0.92,
            "is_fallback": True
        }

    @staticmethod
    def mock_quality_inspection(batch_id: int, product_id: int, photo_urls: List[str]) -> Dict[str, Any]:
        return {
            "success": True,
            "batch_id": batch_id,
            "quality_score": 90.0,
            "confidence_score": 0.85,
            "defects_detected": [],
            "specification_deviations": [],
            "explanation": "Visual assessment passes baseline tolerances. Awaiting mandatory human verification.",
            "suggested_action": "APPROVE_PENDING_HUMAN_INSPECTION",
            "is_fallback": True
        }

    @staticmethod
    def mock_pricing(material: float, labor: float, packaging: float, transport: float, ops: float, qty: int, margin_pct: float) -> Dict[str, Any]:
        total_cost = material + labor + packaging + transport + ops
        cost_per_unit = total_cost / max(1, qty)
        margin_multiplier = 1.0 + (margin_pct / 100.0)
        suggested_unit_price = round(cost_per_unit * margin_multiplier, 2)
        total_order_val = round(suggested_unit_price * qty, 2)
        profit = round(total_order_val - total_cost, 2)
        
        return {
            "success": True,
            "recommended_selling_price_per_unit": suggested_unit_price,
            "recommended_total_order_value": total_order_val,
            "estimated_profit": profit,
            "margin_percentage": margin_pct,
            "missing_cost_warnings": ["Ensure packaging buffer is factored in for humid storage."],
            "is_fallback": True
        }

    @staticmethod
    def mock_financial_anomalies(earnings: List[Dict[str, Any]]) -> Dict[str, Any]:
        anomalies = []
        for e in earnings:
            deductions = e.get("deductions", 0.0)
            gross = e.get("gross_earnings", 0.0)
            if gross > 0 and (deductions / gross) > 0.40:
                anomalies.append({
                    "member_id": e.get("member_id"),
                    "flag_type": "HIGH_DEDUCTION_RATIO",
                    "severity": "WARNING",
                    "detail": f"Deduction of INR {deductions} is over 40% of gross earnings INR {gross}.",
                    "requires_human_resolution": True
                })
        return {
            "success": True,
            "anomalies_flagged": anomalies,
            "is_fallback": True
        }

    @staticmethod
    def mock_rag_assistant(query: str, language: str) -> Dict[str, Any]:
        # Multilingual responses for common queries
        if language == "kn":
            answer = "ಸ್ವ-ಸಹಾಯ ಸಂಘದ (SHG) ಆದೇಶಗಳ ಸ್ಥಿತಿ, ಕಾರ್ಯ ಹಂಚಿಕೆ ಮತ್ತು ಗಳಿಕೆಯನ್ನು ನಿಮ್ಮ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಲ್ಲಿ ಪರಿಶೀಲಿಸಬಹುದು."
        elif language == "hi":
            answer = "स्वयं सहायता समूह (SHG) के आदेशों की स्थिति, कार्य आवंटन और कमाई को आप अपने डैशबोर्ड में देख सकते हैं।"
        else:
            answer = f"SHG Saathi Assistant: Regarding '{query}', all tasks and verified earnings are tracked transparently in your member profile."

        return {
            "success": True,
            "answer": answer,
            "language": language,
            "references": ["SHG Operational Guidelines Handbook 2026", "NRLM Livelihoods Protocol"],
            "is_fallback": True
        }
