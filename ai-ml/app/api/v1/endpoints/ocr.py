from fastapi import APIRouter, Depends
from app.core.security import verify_service_key
from app.schemas.ocr import OCRRequest, OCRResponse
from app.services.ocr_service import ocr_service

router = APIRouter()


@router.post(
    "/ocr/extract",
    response_model=OCRResponse,
    summary="Extract structured data from documents (PO, Invoice, Bills)",
    description="Performs OCR and field extraction on commercial documents with confidence scoring."
)
def extract_document(
    request: OCRRequest,
    _auth: str = Depends(verify_service_key)
) -> OCRResponse:
    """Extracts buyer name, PO number, line items, and totals from uploaded documents."""
    return ocr_service.extract_document(request)

