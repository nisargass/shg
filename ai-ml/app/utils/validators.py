import re
from typing import Set
from fastapi import HTTPException, status
from app.core.config import settings

VALID_PINCODE_REGEX = re.compile(r"^[1-9][0-9]{5}$")
ALLOWED_DOCUMENT_MIMES: Set[str] = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/webp"
}
ALLOWED_AUDIO_MIMES: Set[str] = {
    "audio/wav",
    "audio/x-wav",
    "audio/mpeg",
    "audio/mp3",
    "audio/m4a",
    "audio/x-m4a",
    "audio/ogg"
}
SUPPORTED_LANGUAGES: Set[str] = {"en", "kn", "hi"}


def validate_pincode(pincode: str, field_name: str = "pincode") -> str:
    """Validates that a string is a valid 6-digit Indian Postal PIN code."""
    cleaned = str(pincode).strip()
    if not VALID_PINCODE_REGEX.match(cleaned):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Indian PIN code for '{field_name}': '{pincode}'. Must be a 6-digit number starting with 1-9."
        )
    return cleaned


def validate_file_size_and_mime(file_bytes: bytes, mime_type: str, allowed_mimes: Set[str]) -> None:
    """Ensures file does not exceed size limits and conforms to allowed MIME types."""
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Uploaded file exceeds maximum limit of {settings.MAX_UPLOAD_SIZE_MB}MB"
        )
    if mime_type.lower() not in allowed_mimes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file MIME type '{mime_type}'. Allowed types: {list(allowed_mimes)}"
        )


def validate_language_code(language: str) -> str:
    """Validates that requested language is supported (en, kn, hi)."""
    lang = language.strip().lower()
    if lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported language code '{language}'. Supported languages: {list(SUPPORTED_LANGUAGES)}"
        )
    return lang

