from src.adapters.openai import OpenAIResponder
from src.core.interfaces import LLMInteraction


def get_llm_responder() -> LLMInteraction:
    return OpenAIResponder()
