from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class QualityStatus(str, Enum):
    PENDING_INSPECTION = "PENDING_INSPECTION"
    AI_ANALYSIS_COMPLETED = "AI_ANALYSIS_COMPLETED"
    PENDING_HUMAN_REVIEW = "PENDING_HUMAN_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REWORK_REQUIRED = "REWORK_REQUIRED"


class QualityInspection(Base):
    __tablename__ = "quality_inspections"

    id = Column(Integer, primary_key=True, index=True)
    production_batch_id = Column(Integer, ForeignKey("production_batches.id"), nullable=False, unique=True)
    inspector_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(50), default=QualityStatus.PENDING_INSPECTION.value, nullable=False, index=True)
    
    # AI Inspection Output (Separate from human decisions)
    ai_score = Column(Float, nullable=True)
    ai_defects_detected = Column(Text, nullable=True, default="[]")  # JSON list
    ai_explanation = Column(Text, nullable=True)
    ai_suggested_action = Column(String(100), nullable=True)
    
    # Verified Human Decisions
    human_decision = Column(String(50), nullable=True)  # APPROVED, REJECTED, REWORK_REQUIRED
    human_reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    batch = relationship("ProductionBatch", back_populates="inspection")
    reviewer = relationship("User", foreign_keys=[human_reviewer_id])
