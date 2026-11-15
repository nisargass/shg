from fastapi import APIRouter, Depends
from app.core.security import verify_service_key
from app.schemas.translation import TranslationRequest, TranslationResponse
from app.services.translation_service import translation_service

router = APIRouter()


@router.post(
    "/translate",
    response_model=TranslationResponse,
    summary="Multilingual translation with numerical preservation",
    description="Translates operational instructions and status updates into Kannada, Hindi, and English while strictly preserving quantities, dates, and amounts."
)
def translate_text(
    request: TranslationRequest,
    _auth: str = Depends(verify_service_key)
) -> TranslationResponse:
    """Returns translations dictionary mapping target language codes to translated text."""
    return translation_service.translate_text(request)

