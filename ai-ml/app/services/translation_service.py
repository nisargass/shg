from app.providers.translation_provider import get_translation_provider
from app.schemas.translation import TranslationRequest, TranslationResponse


class TranslationService:
    def __init__(self):
        self.provider = get_translation_provider()

    def translate_text(self, req: TranslationRequest) -> TranslationResponse:
        translations = self.provider.translate(
            text=req.text,
            target_languages=req.target_languages
        )
        return TranslationResponse(
            success=True,
            translations=translations
        )


translation_service = TranslationService()

