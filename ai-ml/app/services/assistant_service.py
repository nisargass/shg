from typing import List, Tuple
from app.providers.llm_provider import get_llm_provider
from app.rag.retriever import rag_retriever
from app.schemas.assistant import AssistantQueryRequest, AssistantQueryResponse


class AssistantService:
    def __init__(self):
        self.retriever = rag_retriever
        self.llm_provider = get_llm_provider()

    def answer_query(self, req: AssistantQueryRequest) -> AssistantQueryResponse:
        # Step 1: Semantic retrieval from knowledge base
        retrieved_results = self.retriever.retrieve(
            query=req.query,
            top_k=3,
            min_score_threshold=0.08
        )

        references: List[str] = []
        context_chunks: List[str] = []

        for chunk_data, score in retrieved_results:
            title = chunk_data.get("title", chunk_data.get("source", "SHG Saathi Knowledge Base"))
            source_file = chunk_data.get("source", "")
            ref_str = f"{title} ({source_file})" if source_file else title
            if ref_str not in references:
                references.append(ref_str)
            context_chunks.append(chunk_data.get("text", ""))

        # Check if query is privacy-violating for an individual member
        # (e.g. asking for another member's financial balance)
        query_lower = req.query.lower()
        if req.user_role == "SHG_MEMBER":
            if "other member" in query_lower or "someone else" in query_lower or "member 2" in query_lower:
                return AssistantQueryResponse(
                    success=True,
                    answer="Under SHG privacy guidelines, members can only view their own individual allocations and verified earnings.",
                    language=req.language,
                    references=["SHG Governance and Data Privacy SOP"],
                    confidence_score=0.99
                )

        # Step 2: Grounded answer generation via LLM provider
        answer = self.llm_provider.generate_answer(
            query=req.query,
            context_chunks=context_chunks,
            user_role=req.user_role or "SHG_MEMBER",
            language=req.language
        )

        confidence = 0.92 if context_chunks else 0.40

        return AssistantQueryResponse(
            success=True,
            answer=answer,
            language=req.language,
            references=references if context_chunks else [],
            confidence_score=confidence
        )


assistant_service = AssistantService()

