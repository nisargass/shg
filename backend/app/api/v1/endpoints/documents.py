from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.support import Document, DocumentType, OCRStatus
from app.models.user import User
from app.schemas.support import DocumentOut, DocumentVerifyRequest
from app.schemas.common import APIResponse
from app.services.document_service import DocumentService
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/upload", response_model=APIResponse[DocumentOut], status_code=status.HTTP_201_CREATED)
def upload_document(
    title: str = Form(...),
    document_type: DocumentType = Form(DocumentType.PURCHASE_ORDER),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Uploads a document (PDF, PNG, JPEG), validates size/type, runs AI OCR, and marks as NEEDS_REVIEW."""
    doc = DocumentService.save_and_process_document(
        db=db,
        uploaded_by_id=current_user.id,
        title=title,
        doc_type=document_type,
        file=file
    )
    return APIResponse(
        success=True,
        message="Document uploaded and AI OCR extraction completed in NEEDS_REVIEW status.",
        data=DocumentOut.model_validate(doc)
    )


@router.put("/{document_id}/verify", response_model=APIResponse[DocumentOut])
def verify_document_data(
    document_id: int,
    verify_in: DocumentVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER, UserRole.BUYER))
):
    """Authorized user verifies and corrects OCR extracted fields, converting status to VERIFIED."""
    doc = DocumentService.verify_document(
        db=db,
        document_id=document_id,
        verified_by_id=current_user.id,
        verify_in=verify_in
    )
    return APIResponse(
        success=True,
        message="Document extracted data verified and approved by human reviewer",
        data=DocumentOut.model_validate(doc)
    )


@router.get("/{document_id}", response_model=APIResponse[DocumentOut])
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves document record with OCR status and extracted data."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return APIResponse(
        success=True,
        message="Document retrieved",
        data=DocumentOut.model_validate(doc)
    )
