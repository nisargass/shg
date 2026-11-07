import json
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.quality import QualityInspection, QualityStatus
from app.models.work import ProductionBatch, BatchStatus, WorkAllocation
from app.models.order import ProductSpecification, OrderItem
from app.models.support import Notification
from app.schemas.quality import QualityReviewRequest
from app.services.ai_client import ai_service_client


class QualityService:

    @staticmethod
    def run_ai_inspection(db: Session, inspection_id: int) -> QualityInspection:
        inspection = db.query(QualityInspection).filter(QualityInspection.id == inspection_id).first()
        if not inspection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quality inspection record not found")

        batch = inspection.batch
        if not batch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated batch not found")

        # Gather specifications for the product
        alloc = db.query(WorkAllocation).filter(WorkAllocation.id == batch.work_allocation_id).first()
        product_id = alloc.order_item.product_id if alloc and alloc.order_item else 1

        specs = db.query(ProductSpecification).filter(ProductSpecification.product_id == product_id).all()
        specs_list = [
            {
                "parameter_name": s.parameter_name,
                "target_value": s.target_value,
                "tolerance_range": s.tolerance_range
            }
            for s in specs
        ]

        photos = []
        if batch.photo_urls:
            try:
                photos = json.loads(batch.photo_urls)
            except Exception:
                photos = [batch.photo_urls]

        # Call AI CV Quality Inspection
        ai_result = ai_service_client.inspect_batch_quality(
            batch_id=batch.id,
            product_id=product_id,
            photo_urls=photos,
            specifications=specs_list,
            db=db
        )

        inspection.ai_score = ai_result.get("quality_score", 85.0)
        inspection.ai_defects_detected = json.dumps(ai_result.get("defects_detected", []))
        inspection.ai_explanation = ai_result.get("explanation", "")
        inspection.ai_suggested_action = ai_result.get("suggested_action", "PENDING_HUMAN_REVIEW")
        
        # State transitions to PENDING_HUMAN_REVIEW (AI CANNOT decide final rejection!)
        inspection.status = QualityStatus.PENDING_HUMAN_REVIEW.value
        batch.status = BatchStatus.INSPECTED.value

        db.commit()
        db.refresh(inspection)
        return inspection

    @staticmethod
    def submit_human_decision(
        db: Session,
        inspection_id: int,
        reviewer_id: int,
        review_in: QualityReviewRequest
    ) -> QualityInspection:
        inspection = db.query(QualityInspection).filter(QualityInspection.id == inspection_id).first()
        if not inspection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quality inspection record not found")

        valid_decisions = ["APPROVED", "REJECTED", "REWORK_REQUIRED"]
        decision_upper = review_in.human_decision.upper()
        if decision_upper not in valid_decisions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid quality decision '{review_in.human_decision}'. Allowed: {valid_decisions}"
            )

        if decision_upper in ["REJECTED", "REWORK_REQUIRED"] and not review_in.rejection_reason:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A detailed reason is mandatory for rejection or rework requests"
            )

        inspection.human_decision = decision_upper
        inspection.human_reviewer_id = reviewer_id
        inspection.rejection_reason = review_in.rejection_reason
        inspection.reviewed_at = datetime.now(timezone.utc)
        inspection.status = QualityStatus(decision_upper).value

        # Update batch status
        batch = inspection.batch
        if batch:
            if decision_upper == "APPROVED":
                batch.status = BatchStatus.ACCEPTED.value
            elif decision_upper == "REJECTED":
                batch.status = BatchStatus.REJECTED.value
            elif decision_upper == "REWORK_REQUIRED":
                batch.status = BatchStatus.REWORK_REQUIRED.value

            # Notify member of quality decision
            alloc = batch.allocation
            if alloc and alloc.member:
                notif = Notification(
                    user_id=alloc.member.user_id,
                    title=f"Quality Review Decision: {decision_upper}",
                    message=f"Batch {batch.batch_number} has been marked as {decision_upper}. Notes: {review_in.rejection_reason or 'Meets quality standards.'}",
                    notification_type="QUALITY_DECISION",
                    reference_id=batch.id,
                    reference_type="ProductionBatch"
                )
                db.add(notif)

        db.commit()
        db.refresh(inspection)
        return inspection
