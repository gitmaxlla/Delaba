from abc import ABC, abstractmethod
from src.schemas.llm import LLMResponse


class LLMInteraction(ABC):
    @abstractmethod
    def answer(self, query: str) -> LLMResponse:
        pass

    @abstractmethod
    def healthcheck(self) -> bool:
        pass
