import os
import json
import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.support import Document, DocumentType, OCRStatus
from app.schemas.support import DocumentVerifyRequest
from app.services.ai_client import ai_service_client

ALLOWED_MIME_TYPES = [
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/webp"
]


class DocumentService:

    @staticmethod
    def save_and_process_document(
        db: Session,
        uploaded_by_id: int,
        title: str,
        doc_type: DocumentType,
        file: UploadFile
    ) -> Document:
        # Validate mime type
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type '{file.content_type}'. Allowed: {ALLOWED_MIME_TYPES}"
            )

        # Read file bytes & validate size
        file_bytes = file.file.read()
        file_size = len(file_bytes)
        max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB"
            )

        # Save to disk securely
        ext = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        target_path = os.path.join(settings.UPLOAD_DIR, unique_name)
        with open(target_path, "wb") as f:
            f.write(file_bytes)

        # Create Document record with initial PENDING status
        doc = Document(
            title=title,
            document_type=doc_type.value,
            file_url=f"/uploads/{unique_name}",
            file_size_bytes=file_size,
            mime_type=file.content_type,
            uploaded_by_id=uploaded_by_id,
            ocr_status=OCRStatus.PENDING.value
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        # Send to AI OCR microservice
        try:
            ocr_res = ai_service_client.extract_document_ocr(
                document_id=doc.id,
                document_type=doc.document_type,
                file_url=doc.file_url,
                mime_type=doc.mime_type,
                db=db
            )
            # Store extracted information as NEEDS_REVIEW (NEVER verified automatically)
            doc.extracted_data_json = json.dumps(ocr_res.get("extracted_data", {}))
            doc.ocr_status = OCRStatus.NEEDS_REVIEW.value
        except Exception:
            doc.ocr_status = OCRStatus.FAILED.value

        db.commit()
        db.refresh(doc)
        return doc

    @staticmethod
    def verify_document(
        db: Session,
        document_id: int,
        verified_by_id: int,
        verify_in: DocumentVerifyRequest
    ) -> Document:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        # Validate verified json format
        try:
            json.loads(verify_in.verified_data_json)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON format for verified data")

        doc.verified_data_json = verify_in.verified_data_json
        doc.verified_by_id = verified_by_id
        doc.ocr_status = OCRStatus.VERIFIED.value

        db.commit()
        db.refresh(doc)
        return doc
