from typing import Dict, List
from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Source text to translate")
    target_languages: List[str] = Field(..., min_length=1, description="List of target language codes e.g. ['kn', 'hi']")


class TranslationResponse(BaseModel):
    success: bool = True
    translations: Dict[str, str] = Field(..., description="Map of language_code -> translated_text")

