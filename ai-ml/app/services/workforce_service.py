from app.schemas.workforce import WorkforceLikelihoodRequest, WorkforceLikelihoodResponse
from app.services.allocation_optimizer import allocation_optimizer


class WorkforceService:
    def predict_completion_likelihood(self, req: WorkforceLikelihoodRequest) -> WorkforceLikelihoodResponse:
        res = allocation_optimizer.predict_member_completion(
            member_id=req.member_id,
            product_id=req.product_id,
            proposed_quantity=req.proposed_quantity,
            deadline_str=req.deadline,
            available_hours_per_day=req.available_hours_per_day,
            current_workload=req.current_workload,
            historical_completion_rate=req.historical_completion_rate,
            skills=req.skills
        )
        return WorkforceLikelihoodResponse(
            success=True,
            member_id=res["member_id"],
            completion_likelihood_percentage=res["completion_likelihood_percentage"],
            estimated_completion_date=res["estimated_completion_date"],
            confidence_score=res["confidence_score"],
            factors=res["factors"],
            explanation=res["explanation"]
        )


workforce_service = WorkforceService()
