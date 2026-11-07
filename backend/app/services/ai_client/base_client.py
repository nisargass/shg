import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import httpx
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.support import AIAnalysisRecord
from app.services.ai_client.fallback_mock import FallbackAIMockService

logger = logging.getLogger(__name__)


class AIServiceException(Exception):
    def __init__(self, message: str, status_code: int = 503):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class AIServiceClient:
    """Dedicated integration adapter for the AI/ML microservice."""

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[float] = None):
        self.base_url = base_url or settings.AI_SERVICE_BASE_URL
        self.timeout = timeout or settings.AI_SERVICE_TIMEOUT_SECONDS

    def _record_audit(
        self,
        db: Optional[Session],
        capability: str,
        ref_id: Optional[int],
        ref_type: Optional[str],
        req_payload: Dict[str, Any],
        res_payload: Dict[str, Any],
        status: str,
        confidence: Optional[float] = None
    ) -> Optional[AIAnalysisRecord]:
        if not db:
            return None
        try:
            record = AIAnalysisRecord(
                capability_type=capability,
                reference_id=ref_id,
                reference_type=ref_type,
                request_payload_json=json.dumps(req_payload),
                response_payload_json=json.dumps(res_payload),
                confidence_score=confidence,
                status=status
            )
            db.add(record)
            db.commit()
            db.refresh(record)
            return record
        except Exception as e:
            logger.error(f"Failed to record AI analysis audit: {e}")
            if db:
                db.rollback()
            return None

    def post(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        capability: str,
        ref_id: Optional[int] = None,
        ref_type: Optional[str] = None,
        db: Optional[Session] = None,
        fallback_fn: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Executes a POST request to the external AI/ML microservice with fallbacks and audit logging."""
        # If external AI microservice URL is not configured or set to 'mock', use local fallback provider
        base_clean = (self.base_url or "").strip().lower()
        if (not base_clean or base_clean == "mock") and fallback_fn and settings.AI_SERVICE_USE_MOCK_FALLBACK:
            fallback_result = fallback_fn()
            self._record_audit(
                db=db,
                capability=f"{capability}_FALLBACK",
                ref_id=ref_id,
                ref_type=ref_type,
                req_payload=payload,
                res_payload=fallback_result,
                status="FALLBACK_SERVED",
                confidence=fallback_result.get("confidence_score", 0.8)
            )
            return fallback_result

        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            timeout_config = httpx.Timeout(self.timeout, connect=1.0)
            with httpx.Client(timeout=timeout_config) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # Record successful inference
                self._record_audit(
                    db=db,
                    capability=capability,
                    ref_id=ref_id,
                    ref_type=ref_type,
                    req_payload=payload,
                    res_payload=data,
                    status="SUCCESS",
                    confidence=data.get("confidence_score")
                )
                return data

        except (httpx.RequestError, httpx.HTTPStatusError, httpx.TimeoutException) as ex:
            logger.warning(f"AI Microservice connection error at {url}: {ex}")
            
            # Record failed inference
            self._record_audit(
                db=db,
                capability=capability,
                ref_id=ref_id,
                ref_type=ref_type,
                req_payload=payload,
                res_payload={"error": str(ex)},
                status="TIMEOUT" if isinstance(ex, httpx.TimeoutException) else "FAILED",
                confidence=None
            )
            
            if settings.AI_SERVICE_USE_MOCK_FALLBACK and fallback_fn:
                logger.info(f"Falling back to local heuristic provider for '{capability}'.")
                fallback_result = fallback_fn()
                # Record fallback usage
                self._record_audit(
                    db=db,
                    capability=f"{capability}_FALLBACK",
                    ref_id=ref_id,
                    ref_type=ref_type,
                    req_payload=payload,
                    res_payload=fallback_result,
                    status="FALLBACK_SERVED",
                    confidence=fallback_result.get("confidence_score", 0.8)
                )
                return fallback_result

            raise AIServiceException(
                f"AI Microservice temporarily unavailable ({str(ex)}). Please proceed with manual operation.",
                status_code=503
            )
