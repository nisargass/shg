import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_production_settings_accept_secure_configuration():
    settings = Settings(
        APP_ENV="production",
        DEBUG=False,
        SHG_SERVICE_KEY="b" * 64,
        CORS_ORIGINS=[],
    )

    assert settings.APP_ENV == "production"


@pytest.mark.parametrize(
    "overrides",
    [
        {"SHG_SERVICE_KEY": "development-only-change-this-before-production"},
        {"CORS_ORIGINS": ["*"]},
        {"CORS_ORIGINS": ["http://localhost:5173"]},
        {"DEBUG": True},
    ],
)
def test_production_settings_reject_insecure_configuration(overrides):
    settings = {
        "APP_ENV": "production",
        "DEBUG": False,
        "SHG_SERVICE_KEY": "b" * 64,
        "CORS_ORIGINS": [],
    }
    settings.update(overrides)

    with pytest.raises(ValidationError):
        Settings(**settings)
