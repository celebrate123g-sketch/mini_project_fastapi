from sqlalchemy import create_engine, select
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column
)

engine = create_engine("sqlite:///requests.db")

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class ChatRequest(Base):
    __tablename__ = "chat_requests"

    id: Mapped[int] = mapped_column(primary_key=True)

    ip_address: Mapped[str] = mapped_column(index=True)

    prompt: Mapped[str]

    response: Mapped[str]


def get_user_requests(ip_address: str):

    with SessionLocal() as session:

        query = select(ChatRequest).filter_by(
            ip_address=ip_address
        )

        result = session.execute(query)

        requests = result.scalars().all()

        return [
            {
                "id": request.id,
                "prompt": request.prompt,
                "response": request.response
            }
            for request in requests
        ]


def add_request_data(
        ip_address: str,
        prompt: str,
        response: str
) -> None:

    with SessionLocal() as session:

        new_request = ChatRequest(
            ip_address=ip_address,
            prompt=prompt,
            response=response,
        )

        session.add(new_request)

        session.commit()