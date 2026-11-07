from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.user import User, SHGMember
from app.models.work import WorkAllocation
from app.models.finance import MemberEarning
from app.schemas.support import AssistantChatRequest, AssistantChatResponse
from app.services.ai_client import ai_service_client


class AssistantService:

    @staticmethod
    def answer_query(db: Session, user: User, chat_in: AssistantChatRequest) -> AssistantChatResponse:
        # Build privacy-scoped context for caller
        user_context: Dict[str, Any] = {
            "user_id": user.id,
            "full_name": user.full_name,
            "role": user.role,
        }

        if user.role == "SHG_MEMBER" and user.member_profile:
            member = user.member_profile
            # Only include this member's own tasks and earnings
            my_allocations = db.query(WorkAllocation).filter(WorkAllocation.member_id == member.id).all()
            user_context["my_active_tasks_count"] = len([a for a in my_allocations if a.status != "COMPLETED"])
            
            my_earnings = db.query(MemberEarning).filter(MemberEarning.member_id == member.id).all()
            user_context["my_total_earned"] = sum(e.net_payable_amount for e in my_earnings)
        elif user.role == "SHG_LEADER" and user.shg_led:
            shg = user.shg_led[0] if user.shg_led else None
            if shg:
                user_context["shg_name"] = shg.name
                user_context["total_members"] = len(shg.members)

        ai_response = ai_service_client.query_rag_assistant(
            query=chat_in.query,
            language=chat_in.language,
            user_context=user_context,
            db=db
        )

        return AssistantChatResponse(
            query=chat_in.query,
            language=chat_in.language,
            answer=ai_response.get("answer", "Here to assist you with SHG Saathi workflows."),
            references=ai_response.get("references", []),
            audio_url=ai_response.get("audio_url")
        )
