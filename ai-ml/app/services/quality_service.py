from app.providers.vision_provider import get_vision_provider
from app.schemas.quality import DefectItem, QualityInspectionRequest, QualityInspectionResponse, SpecificationDeviation


class QualityService:
    def __init__(self):
        self.provider = get_vision_provider()

    def inspect_batch(self, req: QualityInspectionRequest) -> QualityInspectionResponse:
        specs_data = [s.model_dump() for s in req.specifications]
        res = self.provider.inspect_photos(
            photo_urls=req.photo_urls,
            specifications=specs_data
        )

        defects = [
            DefectItem(
                type=d.get("type", "minor_visual_variance"),
                location=d.get("location", "photo"),
                severity=d.get("severity", "LOW")
            )
            for d in res.get("defects_detected", [])
        ]

        deviations = [
            SpecificationDeviation(
                parameter_name=dev.get("parameter_name", "Specification"),
                observed_value=dev.get("observed_value", "Pending check"),
                status=dev.get("status", "DEVIATION")
            )
            for dev in res.get("specification_deviations", [])
        ]

        return QualityInspectionResponse(
            success=True,
            batch_id=req.batch_id,
            quality_score=res.get("quality_score", 85.0),
            confidence_score=res.get("confidence_score", 0.88),
            detected_issues=res.get("detected_issues", []),
            defects_detected=defects,
            specification_deviations=deviations,
            explanation=res.get("explanation", "Quality inspection complete. Human review required."),
            suggested_action=res.get("suggested_action", "HUMAN_REVIEW"),
            image_quality_status=res.get("image_quality_status", "ACCEPTABLE"),
            review_required=True
        )


quality_service = QualityService()
