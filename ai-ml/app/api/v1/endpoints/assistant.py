from fastapi import APIRouter, Depends
from app.core.security import verify_service_key
from app.schemas.assistant import AssistantQueryRequest, AssistantQueryResponse
from app.services.assistant_service import assistant_service

router = APIRouter()


@router.post(
    "/assistant/query",
    response_model=AssistantQueryResponse,
    summary="Query multilingual RAG knowledge assistant",
    description="Retrieves verified knowledge base guidelines and synthesizes role-aware, grounded responses in English, Kannada, or Hindi."
)
def query_assistant(
    request: AssistantQueryRequest,
    _auth: str = Depends(verify_service_key)
) -> AssistantQueryResponse:
    """Answers operational, scheme, and workflow questions with verified references and strict member privacy."""
    return assistant_service.answer_query(request)

