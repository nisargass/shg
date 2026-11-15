from typing import Optional
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from app.core.security import verify_service_key
from app.schemas.voice import STTRequest, STTResponse, TTSRequest, TTSResponse
from app.services.voice_service import voice_service

router = APIRouter()


@router.post(
    "/voice/stt",
    response_model=STTResponse,
    summary="Speech-to-Text transcription",
    description="Transcribes audio file binary (WAV, MP3, M4A) or base64 JSON payload in Kannada, Hindi, or English."
)
async def speech_to_text(
    request: Request,
    _auth: str = Depends(verify_service_key)
) -> STTResponse:
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        body = await request.json()
        req_obj = STTRequest(**body)
        return voice_service.process_stt(
            audio_base64=req_obj.audio_base64,
            language=req_obj.language
        )
    elif "multipart/form-data" in content_type:
        form = await request.form()
        audio_file = form.get("file")
        language = form.get("language", "kn")
        if not audio_file or not hasattr(audio_file, "read"):
            from app.core.exceptions import InvalidInputException
            raise InvalidInputException("Multipart form-data must include an audio 'file' field.")
        audio_bytes = await audio_file.read()
        return voice_service.process_stt(
            audio_bytes=audio_bytes,
            language=str(language)
        )
    else:
        # Raw audio binary upload
        raw_bytes = await request.body()
        lang = request.query_params.get("language", "kn")
        return voice_service.process_stt(
            audio_bytes=raw_bytes,
            language=lang
        )


@router.post(
    "/voice/tts",
    response_model=TTSResponse,
    summary="Text-to-Speech synthesis",
    description="Converts text into base64 encoded audio in Kannada, Hindi, or English."
)
def text_to_speech(
    request: TTSRequest,
    _auth: str = Depends(verify_service_key)
) -> TTSResponse:
    """Returns base64 encoded audio binary and audio/wav or audio/mp3 MIME type."""
    return voice_service.process_tts(request)

