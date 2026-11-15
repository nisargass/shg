import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.core import security
from app.core.config import settings as app_settings


def test_production_settings_accept_secure_configuration():
    settings = Settings(
        ENV="production",
        DEBUG=False,
        ALLOW_PUBLIC_REGISTRATION=False,
        DATABASE_URL="postgresql+psycopg2://user:password@db:5432/shg",
        SECRET_KEY="a" * 64,
        SHG_SERVICE_KEY="b" * 64,
        AI_SERVICE_USE_MOCK_FALLBACK=False,
        BACKEND_CORS_ORIGINS=["https://app.example.com"],
    )

    assert settings.ENV == "production"


@pytest.mark.parametrize(
    "overrides",
    [
        {"SECRET_KEY": "development-only-change-this-before-production"},
        {"SHG_SERVICE_KEY": "development-only-insecure-service-key"},
        {"BACKEND_CORS_ORIGINS": ["*"]},
        {"BACKEND_CORS_ORIGINS": ["http://app.example.com"]},
        {"BACKEND_CORS_ORIGINS": ["https://app.example.com/path"]},
        {"DATABASE_URL": "sqlite:///./shg_saathi.db"},
        {"DEBUG": True},
        {"ALLOW_PUBLIC_REGISTRATION": True},
        {"AI_SERVICE_USE_MOCK_FALLBACK": True},
        {"SHG_SERVICE_KEY": "a" * 64},
    ],
)
def test_production_settings_reject_insecure_configuration(overrides):
    settings = {
        "ENV": "production",
        "DEBUG": False,
        "ALLOW_PUBLIC_REGISTRATION": False,
        "DATABASE_URL": "postgresql+psycopg2://user:password@db:5432/shg",
        "SECRET_KEY": "a" * 64,
        "SHG_SERVICE_KEY": "b" * 64,
        "AI_SERVICE_USE_MOCK_FALLBACK": False,
        "BACKEND_CORS_ORIGINS": ["https://app.example.com"],
    }
    settings.update(overrides)

    with pytest.raises(ValidationError):
        Settings(**settings)


def test_demo_tokens_are_rejected_in_production(monkeypatch):
    monkeypatch.setattr(app_settings, "ENV", "production")

    assert security.decode_access_token("demo-jwt-token-leader") is None
