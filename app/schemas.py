from pydantic import BaseModel, Field
from datetime import datetime


class PromptRequest(BaseModel):
    prompt: str = Field(
        min_length=1,
        max_length=2000
    )


class PromptResponse(BaseModel):
    answer: str


class ChatHistory(BaseModel):
    id: int
    prompt: str
    response: str
    created_at: datetime