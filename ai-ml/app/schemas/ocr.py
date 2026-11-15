from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class OCRItem(BaseModel):
    product_name: str
    quantity: float
    unit_price: Optional[float] = None
    specifications: Optional[str] = None


class OCRExtractedData(BaseModel):
    buyer_name: Optional[str] = None
    po_number: Optional[str] = None
    order_date: Optional[str] = None
    delivery_deadline: Optional[str] = None
    items: List[OCRItem] = []
    total_amount: Optional[float] = None


class OCRRequest(BaseModel):
    document_id: int = Field(..., description="Unique database ID of document in main backend")
    document_type: str = Field(..., description="PURCHASE_ORDER, INVOICE, MATERIAL_BILL, etc.")
    file_url: str = Field(..., description="Relative or absolute URL of uploaded file")
    mime_type: str = Field(..., description="File MIME type e.g. application/pdf, image/png")


class OCRResponse(BaseModel):
    success: bool = True
    confidence_score: float = Field(..., description="Confidence of extraction between 0.0 and 1.0")
    extracted_data: Dict[str, Any] = Field(..., description="Structured extracted document fields")
    raw_text: str = Field(..., description="Raw optical character text extracted from document")
    notes: Optional[str] = Field(None, description="Diagnostic notes or alerts")
    review_required: bool = Field(True, description="Human review is always mandatory for OCR candidates")

