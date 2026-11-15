import os
import sys
import pytest
from starlette.testclient import TestClient

# Ensure ai-service root is on python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.main import app


@pytest.fixture(scope="session")
def client():
    """Provides real Starlette TestClient instance for full router dispatch."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    return {"X-SHG-Service-Key": settings.SHG_SERVICE_KEY}


@pytest.fixture
def invalid_auth_headers():
    return {"X-SHG-Service-Key": "invalid_wrong_secret_key_12345"}
