from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


class BaseLLMProvider(ABC):
    """Abstract interface for Large Language Model generation."""

    @abstractmethod
    def generate_answer(
        self,
        query: str,
        context_chunks: List[str],
        user_role: str,
        language: str = "en"
    ) -> str:
        """Generates grounded answer using retrieved context chunks."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if provider credentials and network are configured."""
        pass


class BaseVisionProvider(ABC):
    """Abstract interface for Computer Vision quality inspection."""

    @abstractmethod
    def inspect_photos(
        self,
        photo_urls: List[str],
        specifications: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyzes batch photos against product specifications."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if vision inspection engine is active."""
        pass


class BaseSpeechProvider(ABC):
    """Abstract interface for Speech-to-Text transcription."""

    @abstractmethod
    def transcribe(
        self,
        audio_bytes: bytes,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transcribes audio binary into text."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if speech recognition model is loaded or accessible."""
        pass


class BaseTTSProvider(ABC):
    """Abstract interface for Text-to-Speech synthesis."""

    @abstractmethod
    def synthesize(
        self,
        text: str,
        language: str = "kn"
    ) -> Tuple[str, str]:
        """Synthesizes text into base64 encoded audio and returns (base64_data, mime_type)."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if TTS engine is available."""
        pass


class BaseTranslationProvider(ABC):
    """Abstract interface for Multilingual Translation."""

    @abstractmethod
    def translate(
        self,
        text: str,
        target_languages: List[str]
    ) -> Dict[str, str]:
        """Translates text into target languages preserving numerical quantities."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if translation service is ready."""
        pass


class BaseOCRProvider(ABC):
    """Abstract interface for Document Optical Character Recognition."""

    @abstractmethod
    def extract_document(
        self,
        file_path_or_url: str,
        document_type: str,
        mime_type: str
    ) -> Dict[str, Any]:
        """Extracts text and key-value fields from document image or PDF."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if OCR engine is operational."""
        pass

