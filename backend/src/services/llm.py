from src.core.interfaces import LLMInteraction
from src.schemas.llm import LLMResponse


def answer(query: str, responder: LLMInteraction) -> LLMResponse:
    return responder.answer(query)
