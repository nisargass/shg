from typing import Any, Dict, List
from app.schemas.allocation import AllocationRequest, AllocationResponse, MemberAllocationRecommendation
from app.services.allocation_optimizer import allocation_optimizer


class AllocationService:
    def recommend_allocation(self, req: AllocationRequest) -> AllocationResponse:
        members_data = [m.model_dump() for m in req.members]
        res = allocation_optimizer.optimize_allocation(
            bulk_order_id=req.bulk_order_id,
            order_item_id=req.order_item_id,
            product_id=req.product_id,
            total_quantity=req.total_quantity,
            deadline_str=req.deadline,
            members=members_data
        )

        recs = [
            MemberAllocationRecommendation(
                member_id=r["member_id"],
                proposed_quantity=r["proposed_quantity"],
                completion_likelihood_percentage=r["completion_likelihood_percentage"],
                estimated_completion_date=r["estimated_completion_date"],
                confidence_score=r["confidence_score"],
                factors=r["factors"],
                explanation=r["explanation"]
            )
            for r in res.get("recommendations", [])
        ]

        return AllocationResponse(
            success=res.get("success", True),
            bulk_order_id=res["bulk_order_id"],
            order_item_id=res["order_item_id"],
            total_allocated=res["total_allocated"],
            unallocated_quantity=res["unallocated_quantity"],
            recommendations=recs,
            fairness_index=res.get("fairness_index", 0.0),
            explanation=res["explanation"]
        )


allocation_service = AllocationService()
