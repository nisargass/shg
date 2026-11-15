from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard generic envelope for successful microservice responses."""
    success: bool = True
    data: Optional[T] = None
    message: str = "Analysis completed"


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error explanation")


class ErrorResponse(BaseModel):
    """Standard envelope for microservice error responses."""
    success: bool = False
    error: ErrorDetail


class HealthResponse(BaseModel):
    """Health status and diagnostic info."""
    service_name: str
    version: str
    status: str
    environment: str
    providers: Dict[str, str]

