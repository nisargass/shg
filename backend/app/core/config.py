import os
import secrets
from typing import List, Union
from urllib.parse import urlsplit
from pydantic import AnyHttpUrl, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


_backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_default_db_path = os.path.join(_backend_dir, "shg_saathi.db").replace("\\", "/")


class Settings(BaseSettings):
    PROJECT_NAME: str = "SHG Saathi Backend"
    API_V1_STR: str = "/api/v1"
    ENV: str = "development"
    DEBUG: bool = True
    ALLOW_PUBLIC_REGISTRATION: bool = True

    # Database (resolves canonical path to backend/shg_saathi.db for SQLite)
    DATABASE_URL: str = f"sqlite:///{_default_db_path}"

    @field_validator("DATABASE_URL", mode="before")
    def resolve_sqlite_path(cls, v: str) -> str:
        if v and v.startswith("sqlite:///./"):
            rel_file = v[len("sqlite:///./"):]
            abs_file = os.path.join(_backend_dir, rel_file).replace("\\", "/")
            return f"sqlite:///{abs_file}"
        return v

    # JWT Authentication
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # External AI/ML Microservice (Set to 'mock' or omit when microservice is not yet running)
    AI_SERVICE_BASE_URL: str = "http://localhost:8001"
    AI_SERVICE_TIMEOUT_SECONDS: float = 10.0
    AI_SERVICE_USE_MOCK_FALLBACK: bool = True  # Allows local operation without failing if AI server is offline
    SHG_SERVICE_KEY: str = "development-only-insecure-service-key"

    # Uploads
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 25

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
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
        if self.ENV.lower() not in {"production", "prod"}:
            if not self.SECRET_KEY:
                self.SECRET_KEY = secrets.token_urlsafe(32)
            return self

        if (
            len(self.SECRET_KEY) < 32
            or self.SECRET_KEY.startswith(("REPLACE_", "development-only"))
        ):
            raise ValueError("Production requires SECRET_KEY with at least 32 characters")
        if (
            len(self.SHG_SERVICE_KEY) < 32
            or self.SHG_SERVICE_KEY.startswith(("REPLACE_", "development-only"))
        ):
            raise ValueError("Production requires a unique SHG_SERVICE_KEY with at least 32 characters")
        if self.SECRET_KEY == self.SHG_SERVICE_KEY:
            raise ValueError("SECRET_KEY and SHG_SERVICE_KEY must be different values")
        if self.DEBUG:
            raise ValueError("DEBUG must be false in production")
        if self.ALLOW_PUBLIC_REGISTRATION:
            raise ValueError("Public registration must be disabled in production")
        if self.AI_SERVICE_USE_MOCK_FALLBACK:
            raise ValueError("AI_SERVICE_USE_MOCK_FALLBACK must be false in production")
        if not self.DATABASE_URL.startswith(("postgresql://", "postgresql+")):
            raise ValueError("Production requires PostgreSQL; SQLite is for development only")
        if not self.BACKEND_CORS_ORIGINS:
            raise ValueError("Production must configure explicit frontend CORS origins")
        for origin in self.BACKEND_CORS_ORIGINS:
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
                raise ValueError("Production CORS origins must be exact HTTPS frontend origins")
        return self


settings = Settings()

# Ensure uploads folder exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
