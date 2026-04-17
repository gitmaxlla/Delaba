from pydantic import BaseModel


class LLMQuery(BaseModel):
    content: str


class LLMResponse(BaseModel):
    content: str
