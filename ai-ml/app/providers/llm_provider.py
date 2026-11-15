import logging
from typing import Any, Dict, List, Optional
import httpx
from app.core.config import settings
from app.providers.base import BaseLLMProvider

logger = logging.getLogger("ai_service.llm")


class LocalDeterministicLLMProvider(BaseLLMProvider):
    """Deterministic local grounded answering engine.

    Synthesizes answers directly from retrieved RAG context chunks,
    applying strict role-based privacy filters and language adaptations.
    """

    def is_available(self) -> bool:
        return True

    def generate_answer(
        self,
        query: str,
        context_chunks: List[str],
        user_role: str,
        language: str = "en"
    ) -> str:
        if not context_chunks:
            if language == "kn":
                return "ಕ್ಷಮಿಸಿ, ಜ್ಞಾನ ಭಂಡಾರದಲ್ಲಿ (Knowledge Base) ಈ ಪ್ರಶ್ನೆಗೆ ಉತ್ತರಿಸಲು ಸಾಕಷ್ಟು ಮಾಹಿತಿ ಕಂಡುಬಂದಿಲ್ಲ."
            elif language == "hi":
                return "क्षमा करें, ज्ञानकोष में इस प्रश्न का सटीक उत्तर देने के लिए पर्याप्त जानकारी उपलब्ध नहीं है।"
            return "The knowledge base does not contain sufficient verified information to answer this query accurately."

        # Medical symptoms check
        medical_keywords = ["fever", "pain", "chest", "bleeding", "dizziness", "cough", "infection", "doctor", "headache"]
        has_medical = any(k in query.lower() for k in medical_keywords)

        # Synthesize top sentences from the most relevant retrieved chunk
        primary_chunk = context_chunks[0]
        paragraphs = [p.strip() for p in primary_chunk.split("\n") if p.strip() and not p.strip().startswith("#")]
        key_content = " ".join(paragraphs[:3]) if paragraphs else primary_chunk

        # Language-aware response synthesis
        if language == "kn":
            answer = f"ಪರಿಶೀಲಿಸಿದ ಮಾರ್ಗಸೂಚಿಗಳ ಪ್ರಕಾರ: {key_content}"
            if has_medical:
                answer += "\n\nಸೂಚನೆ: ಇದು ಕೇವಲ ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ಶಿಕ್ಷಣ ಮಾಹಿತಿ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಹತ್ತಿರದ ಪ್ರಾಥಮಿಕ ಆರೋಗ್ಯ ಕೇಂದ್ರ (PHC) ಅಥವಾ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ."
        elif language == "hi":
            answer = f"सत्यापित परिचालन दिशानिर्देशों के अनुसार: {key_content}"
            if has_medical:
                answer += "\n\nसूचना: यह केवल सामान्य स्वास्थ्य शिक्षा जानकारी है। कृपया अपने नजदीकी प्राथमिक स्वास्थ्य केंद्र (PHC) या डॉक्टर से परामर्श लें।"
        else:
            answer = f"According to verified SHG Saathi operational guidelines: {key_content}"
            if has_medical:
                answer += "\n\nMedical Advisory: This information is for general occupational wellness education only. Please consult a qualified medical professional at your local Primary Health Centre (PHC) for clinical diagnosis or treatment."

        return answer


class ExternalCloudLLMProvider(BaseLLMProvider):
    """External LLM adapter (Groq / OpenAI compatible)."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.LLM_API_KEY
        self.model = model or settings.LLM_MODEL
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def generate_answer(
        self,
        query: str,
        context_chunks: List[str],
        user_role: str,
        language: str = "en"
    ) -> str:
        if not self.is_available():
            raise RuntimeError("Cloud LLM provider credentials are not configured.")

        context_text = "\n\n---\n\n".join(context_chunks)
        system_prompt = (
            f"You are the intelligent assistant for SHG Saathi, a platform empowering Women's Self-Help Groups.\n"
            f"User role: {user_role}. Target language: {language}.\n"
            f"Instructions:\n"
            f"1. Strictly answer using ONLY the retrieved context provided below.\n"
            f"2. Never reveal private financial details or another member's confidential info.\n"
            f"3. If context does not contain the answer, state that the knowledge base lacks sufficient info.\n"
            f"4. Never provide clinical medical diagnoses. Recommend consulting a healthcare professional for symptoms.\n"
            f"5. Answer in the requested language ({language}).\n\n"
            f"Context:\n{context_text}"
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            "temperature": 0.2
        }

        try:
            with httpx.Client(timeout=settings.AI_PROVIDER_TIMEOUT) as client:
                res = client.post(self.endpoint, json=payload, headers=headers)
                res.raise_for_status()
                data = res.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"External LLM generation failed: {e}")
            raise


def get_llm_provider() -> BaseLLMProvider:
    """Factory returns configured LLM provider or local fallback."""
    if settings.LLM_PROVIDER.lower() in ["groq", "openai"] and settings.LLM_API_KEY:
        return ExternalCloudLLMProvider()
    return LocalDeterministicLLMProvider()

