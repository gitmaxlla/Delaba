from openai import OpenAI
from src.core.exceptions import LLMGenerationError
from src.core.interfaces import LLMInteraction
from src.schemas.llm import LLMResponse
from src.core.config import OPENAI_API_KEY, OPENAI_ENDPOINT, OPENAI_MODEL_TAG


client = OpenAI(base_url=OPENAI_ENDPOINT, api_key=OPENAI_API_KEY)


class OpenAIResponder(LLMInteraction):
    def healthcheck(self) -> bool:
        try:
            client.models.list()
            return True
        except Exception:
            return False

    def answer(self, query: str) -> LLMResponse:
        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL_TAG, messages=[{"role": "user", "content": query}]
            )
        except Exception:
            raise LLMGenerationError("LLM responder failed to generate query response.")

        return LLMResponse(content=str(response.choices[0].message.content))
