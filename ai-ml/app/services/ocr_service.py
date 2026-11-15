from typing import Any, Dict
from app.providers.ocr_provider import get_ocr_provider
from app.schemas.ocr import OCRRequest, OCRResponse


class OCRService:
    def __init__(self):
        self.provider = get_ocr_provider()

    def extract_document(self, req: OCRRequest) -> OCRResponse:
        res = self.provider.extract_document(
            file_path_or_url=req.file_url,
            document_type=req.document_type,
            mime_type=req.mime_type
        )
        return OCRResponse(
            success=res.get("success", True),
            confidence_score=res.get("confidence_score", 0.85),
            extracted_data=res.get("extracted_data", {}),
            raw_text=res.get("raw_text", ""),
            notes=res.get("notes"),
            review_required=res.get("review_required", True)
        )


ocr_service = OCRService()

