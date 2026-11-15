from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator


class AssistantQueryRequest(BaseModel):
    query: str = Field(..., min_length=2, description="User question or query")
    language: str = Field("en", description="Supported language code: 'en', 'kn', or 'hi'")
    user_role: Optional[str] = Field(None, description="SHG_MEMBER, SHG_LEADER, FEDERATION_OFFICER")
    user_context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Contextual user details")

    @model_validator(mode="after")
    def unify_user_role(self):
        if not self.user_role:
            # Check user_context for role
            ctx_role = (self.user_context or {}).get("role")
            self.user_role = ctx_role if ctx_role else "SHG_MEMBER"
        return self


class AssistantQueryResponse(BaseModel):
    success: bool = True
    answer: str
    language: str
    references: List[str] = []
    confidence_score: float = Field(0.90, description="RAG retrieval confidence score")

