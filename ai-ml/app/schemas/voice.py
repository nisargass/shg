from typing import Optional
from pydantic import BaseModel, Field


class STTRequest(BaseModel):
    audio_base64: Optional[str] = Field(None, description="Base64 encoded audio binary for JSON requests")
    language: Optional[str] = Field("kn", description="Language hint: 'kn' (Kannada), 'hi' (Hindi), 'en' (English)")


class STTResponse(BaseModel):
    success: bool = True
    text: str = Field(..., description="Transcribed speech text")
    language: str = Field(..., description="Detected or requested language code")
    confidence_score: float = Field(..., description="Transcription confidence 0.0 to 1.0")


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text string to convert to speech")
    language: str = Field("kn", description="Target audio language: 'kn', 'hi', or 'en'")


class TTSResponse(BaseModel):
    success: bool = True
    audio_base64: str = Field(..., description="Base64 encoded synthesized speech audio")
    mime_type: str = Field("audio/mp3", description="Audio MIME type, e.g. audio/mp3 or audio/wav")

