from typing import Any, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class AIException(Exception):
    """Base exception class for the AI microservice."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class AuthenticationException(AIException):
    """Raised when service-to-service key is missing or invalid."""

    def __init__(self, message: str = "Invalid or missing service authentication key", status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message=message, code="AUTHENTICATION_FAILED", status_code=status_code)


class AIProviderUnavailableException(AIException):
    """Raised when an external AI provider (LLM, Vision, STT, TTS) is not configured or unreachable."""

    def __init__(self, message: str = "The requested AI provider is currently unavailable."):
        super().__init__(message=message, code="PROVIDER_UNAVAILABLE", status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


class AIProviderTimeoutException(AIException):
    """Raised when an external AI inference call exceeds timeout."""

    def __init__(self, message: str = "The AI provider timed out while processing the request."):
        super().__init__(message=message, code="PROVIDER_TIMEOUT", status_code=status.HTTP_504_GATEWAY_TIMEOUT)


class InvalidInputException(AIException):
    """Raised when input parameters fail domain or mathematical constraints."""

    def __init__(self, message: str):
        super().__init__(message=message, code="INVALID_INPUT", status_code=status.HTTP_400_BAD_REQUEST)


async def http_exception_handler(request: Request, exc: Any) -> JSONResponse:
    """Formats HTTPException into standard error envelope while preserving detail."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "BAD_REQUEST" if exc.status_code == 400 else "HTTP_ERROR",
                "message": exc.detail
            },
            "detail": exc.detail
        }
    )


async def ai_exception_handler(request: Request, exc: AIException) -> JSONResponse:
    """Formats AIException into standard error envelope."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Formats Pydantic RequestValidationError into standard error envelope."""
    error_details = []
    for err in exc.errors():
        field = " -> ".join(str(loc) for loc in err.get("loc", []))
        msg = err.get("msg", "Validation error")
        error_details.append(f"{field}: {msg}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "; ".join(error_details)
            }
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Formats uncaught exceptions into standard error envelope."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": f"An unexpected error occurred: {str(exc)}"
            }
        }
    )

