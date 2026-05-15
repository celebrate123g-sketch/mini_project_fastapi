from datetime import datetime

from pydantic import BaseModel, Field


class CreateChatResponse(BaseModel):
    chat_id: int


class SendMessageRequest(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=4000
    )


class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime