from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.support import AssistantChatRequest, AssistantChatResponse
from app.schemas.common import APIResponse
from app.services.assistant_service import AssistantService
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/chat", response_model=APIResponse[AssistantChatResponse])
def chat_with_assistant(
    chat_in: AssistantChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Multilingual AI RAG assistant (Kannada, Hindi, English) providing operational guidance and scheme help."""
    response = AssistantService.answer_query(
        db=db,
        user=current_user,
        chat_in=chat_in
    )
    return APIResponse(
        success=True,
        message="Assistant query processed",
        data=response
    )
