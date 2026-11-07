from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class DocumentType(str, Enum):
    PURCHASE_ORDER = "PURCHASE_ORDER"
    INVOICE = "INVOICE"
    MATERIAL_BILL = "MATERIAL_BILL"
    PRODUCT_SPEC = "PRODUCT_SPEC"
    PRODUCTION_REGISTER = "PRODUCTION_REGISTER"
    DELIVERY_PROOF = "DELIVERY_PROOF"


class OCRStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False, index=True)
    is_read = Column(Boolean, default=False, index=True)
    reference_id = Column(Integer, nullable=True)
    reference_type = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="notifications")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    document_type = Column(String(50), default=DocumentType.PURCHASE_ORDER.value, nullable=False, index=True)
    file_url = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # OCR and AI Extraction Status (NEVER treated as verified without human review)
    ocr_status = Column(String(50), default=OCRStatus.PENDING.value, nullable=False, index=True)
    extracted_data_json = Column(Text, nullable=True)  # AI OCR result
    verified_data_json = Column(Text, nullable=True)   # Human verified data
    verified_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    uploaded_by = relationship("User", foreign_keys=[uploaded_by_id])
    verified_by = relationship("User", foreign_keys=[verified_by_id])


class AIAnalysisRecord(Base):
    __tablename__ = "ai_analysis_records"

    id = Column(Integer, primary_key=True, index=True)
    capability_type = Column(String(50), nullable=False, index=True)
    reference_id = Column(Integer, nullable=True, index=True)
    reference_type = Column(String(50), nullable=True, index=True)
    request_payload_json = Column(Text, nullable=True)
    response_payload_json = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)
    status = Column(String(50), default="SUCCESS", nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    entity_type = Column(String(100), nullable=False, index=True)
    entity_id = Column(Integer, nullable=True, index=True)
    changes_json = Column(Text, nullable=True)
    ip_address = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
