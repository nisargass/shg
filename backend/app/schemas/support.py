from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.support import DocumentType, OCRStatus


class NotificationOut(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    reference_id: Optional[int] = None
    reference_type: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentOut(BaseModel):
    id: int
    title: str
    document_type: DocumentType
    file_url: str
    file_size_bytes: int
    mime_type: str
    uploaded_by_id: int
    ocr_status: OCRStatus
    extracted_data_json: Optional[str] = None
    verified_data_json: Optional[str] = None
    verified_by_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentVerifyRequest(BaseModel):
    verified_data_json: str = Field(..., description="JSON string of human-verified fields")


class AIAnalysisRecordOut(BaseModel):
    id: int
    capability_type: str
    reference_id: Optional[int] = None
    reference_type: Optional[str] = None
    request_payload_json: Optional[str] = None
    response_payload_json: Optional[str] = None
    confidence_score: Optional[float] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogOut(BaseModel):
    id: int
    user_id: Optional[int] = None
    action: str
    entity_type: str
    entity_id: Optional[int] = None
    changes_json: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AssistantChatRequest(BaseModel):
    query: str
    language: str = Field("en", description="Supported: kn (Kannada), hi (Hindi), en (English)")


class AssistantChatResponse(BaseModel):
    query: str
    language: str
    answer: str
    references: List[str] = []
    audio_url: Optional[str] = None


class FinancialAnomalyReport(BaseModel):
    shg_id: int
    anomalies_detected: int
    details: List[Dict[str, Any]] = []
    status: str = "NEEDS_REVIEW"
