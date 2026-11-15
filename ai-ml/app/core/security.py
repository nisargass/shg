import secrets
from typing import Optional
from fastapi import Header, status
from app.core.config import settings
from app.core.exceptions import AuthenticationException


def verify_service_key(
    x_shg_service_key: Optional[str] = Header(None, alias="X-SHG-Service-Key"),
    x_service_key: Optional[str] = Header(None, alias="X-Service-Key")
) -> str:
    """Verifies that the request carries a valid internal service key.
    Uses constant-time comparison to prevent timing attacks.
    - Missing header returns HTTP 401 UNAUTHORIZED
    - Incorrect header returns HTTP 403 FORBIDDEN
    """
    key = x_shg_service_key or x_service_key
    if not key:
        raise AuthenticationException(
            message="Missing required authentication header 'X-SHG-Service-Key'",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    expected_key = settings.SHG_SERVICE_KEY
    if not expected_key:
        # Fallback if server misconfigured
        raise AuthenticationException(
            message="Server security key is not configured",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Constant time comparison
    is_valid = secrets.compare_digest(
        key.encode("utf-8"),
        expected_key.encode("utf-8")
    )

    if not is_valid:
        raise AuthenticationException(
            message="Invalid service authentication key",
            status_code=status.HTTP_403_FORBIDDEN
        )

    return x_shg_service_key

