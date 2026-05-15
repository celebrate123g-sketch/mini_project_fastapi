from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from datetime import datetime

from db import Base


class ChatRequest(Base):
    __tablename__ = "chat_requests"

    id: Mapped[int] = mapped_column(primary_key=True)

    ip_address: Mapped[str] = mapped_column(
        String,
        index=True
    )

    prompt: Mapped[str]

    response: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    ip_address: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id")
    )

    role: Mapped[str]
    content: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )