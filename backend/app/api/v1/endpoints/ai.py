from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.support import AIAnalysisRecord
from app.models.user import User
from app.schemas.support import AIAnalysisRecordOut
from app.schemas.common import APIResponse
from app.api.deps import require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.get("/audit-records", response_model=APIResponse[List[AIAnalysisRecordOut]])
def get_ai_audit_records(
    capability: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Retrieves full audit records of AI/ML microservice interactions, payloads, confidence scores, and status."""
    query = db.query(AIAnalysisRecord)
    if capability:
        query = query.filter(AIAnalysisRecord.capability_type == capability)
    records = query.order_by(AIAnalysisRecord.created_at.desc()).limit(100).all()

    return APIResponse(
        success=True,
        message="AI audit records retrieved",
        data=[AIAnalysisRecordOut.model_validate(r) for r in records]
    )
