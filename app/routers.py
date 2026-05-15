from fastapi import (
    APIRouter,
    Request,
    HTTPException
)

from sqlalchemy import select

from app.db import SessionLocal

from app.models import (
    Chat,
    Message
)

from app.schemas import (
    CreateChatResponse,
    SendMessageRequest
)

from app.services.gemini_service import (
    get_answer_from_gemini
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/create",
    response_model=CreateChatResponse
)
def create_chat(request: Request):

    user_ip = request.client.host

    with SessionLocal() as session:

        new_chat = Chat(
            ip_address=user_ip
        )

        session.add(new_chat)

        session.commit()

        session.refresh(new_chat)

        return {
            "chat_id": new_chat.id
        }


@router.post("/{chat_id}/message")
def send_message(
    chat_id: int,
    data: SendMessageRequest
):

    with SessionLocal() as session:

        chat = session.get(
            Chat,
            chat_id
        )

        if not chat:
            raise HTTPException(
                status_code=404,
                detail="Chat not found"
            )

        user_message = Message(
            chat_id=chat_id,
            role="user",
            content=data.content
        )

        session.add(user_message)

        session.commit()

        query = (
            select(Message)
            .filter_by(chat_id=chat_id)
            .order_by(Message.id)
        )

        result = session.execute(query)

        messages = result.scalars().all()

        context = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages[-10:]
        ]

        answer = get_answer_from_gemini(
            context
        )

        ai_message = Message(
            chat_id=chat_id,
            role="assistant",
            content=answer
        )

        session.add(ai_message)

        session.commit()

        return {
            "answer": answer
        }


@router.get("/{chat_id}/messages")
def get_messages(chat_id: int):

    with SessionLocal() as session:

        query = (
            select(Message)
            .filter_by(chat_id=chat_id)
            .order_by(Message.id)
        )

        result = session.execute(query)

        messages = result.scalars().all()

        return [
            {
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at
            }
            for msg in messages
        ]