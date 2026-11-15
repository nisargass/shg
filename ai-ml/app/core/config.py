import os
from typing import List, Optional
from urllib.parse import urlsplit
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


class Settings(BaseSettings):
    """Application settings for SHG Saathi AI Microservice.

    Loads from environment variables or a local .env file.
    """

    APP_NAME: str = "SHG Saathi AI Microservice"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8001

    # Security: internal service-to-service key
    SHG_SERVICE_KEY: str = "development-only-insecure-service-key"

    # External Provider Configurations (optional, fallback to local/deterministic)
    LLM_PROVIDER: str = "local"
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "llama-3.1-70b-versatile"

    VISION_PROVIDER: str = "local"
    VISION_API_KEY: Optional[str] = None

    OCR_PROVIDER: str = "local"
    OCR_API_KEY: Optional[str] = None

    SPEECH_PROVIDER: str = "local"
    SPEECH_API_KEY: Optional[str] = None

    TRANSLATION_PROVIDER: str = "local"
    TRANSLATION_API_KEY: Optional[str] = None

    # Knowledge Base & RAG settings
    KNOWLEDGE_BASE_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "knowledge_base"
    )
    AI_PROVIDER_TIMEOUT: float = 15.0
    MAX_UPLOAD_SIZE_MB: int = 25

    # CORS origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.APP_ENV.lower() not in {"production", "prod"}:
            return self
        if (
            len(self.SHG_SERVICE_KEY) < 32
            or self.SHG_SERVICE_KEY.startswith(("REPLACE_", "development-only"))
        ):
            raise ValueError("Production requires a unique SHG_SERVICE_KEY with at least 32 characters")
        if self.DEBUG:
            raise ValueError("DEBUG must be false in production")
        for origin in self.CORS_ORIGINS:
            parsed_origin = urlsplit(origin)
            if (
                parsed_origin.scheme != "https"
                or not parsed_origin.netloc
                or parsed_origin.path
                or parsed_origin.query
                or parsed_origin.fragment
                or "localhost" in parsed_origin.netloc
                or "127.0.0.1" in parsed_origin.netloc
            ):
                raise ValueError("Production CORS origins must be exact HTTPS origins")
        return self


settings = Settings()

