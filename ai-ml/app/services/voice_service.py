import base64
from typing import Optional
from app.core.exceptions import AIProviderUnavailableException, InvalidInputException
from app.providers.speech_provider import get_speech_provider, get_tts_provider
from app.schemas.voice import STTRequest, STTResponse, TTSRequest, TTSResponse
from app.utils.validators import validate_language_code


class VoiceService:
    def __init__(self):
        self.speech_provider = get_speech_provider()
        self.tts_provider = get_tts_provider()

    def process_stt(
        self,
        audio_bytes: Optional[bytes] = None,
        audio_base64: Optional[str] = None,
        language: Optional[str] = "kn"
    ) -> STTResponse:
        lang = validate_language_code(language or "kn")

        data: bytes
        if audio_bytes:
            data = audio_bytes
        elif audio_base64:
            try:
                data = base64.b64decode(audio_base64)
            except Exception:
                raise InvalidInputException("Invalid base64 encoding for audio payload.")
        else:
            raise InvalidInputException("Either raw audio binary or 'audio_base64' string must be provided.")

        if len(data) == 0:
            raise InvalidInputException("Audio binary payload is empty.")

        # Real provider check
        if not self.speech_provider.is_available():
            raise AIProviderUnavailableException(
                "Speech-to-Text provider is not available. Please set SPEECH_API_KEY in .env to enable Whisper transcription."
            )

        res = self.speech_provider.transcribe(data, language=lang)
        return STTResponse(
            success=True,
            text=res.get("text", ""),
            language=res.get("language", lang),
            confidence_score=res.get("confidence_score", 0.90)
        )

    def process_tts(self, req: TTSRequest) -> TTSResponse:
        lang = validate_language_code(req.language)
        if not self.tts_provider.is_available():
            raise AIProviderUnavailableException("Text-to-Speech synthesis provider is currently unavailable.")

        b64_audio, mime = self.tts_provider.synthesize(req.text, language=lang)
        return TTSResponse(
            success=True,
            audio_base64=b64_audio,
            mime_type=mime
        )


voice_service = VoiceService()

