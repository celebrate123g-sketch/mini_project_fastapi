from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column


engine = create_engine(url="sqlite:///requests.db")

session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class ChatRequest(Base):
    __tablename__ = "chat_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(index=True)
    prompt: Mapped[str]
    response: Mapped[str]



def get_user_requests(ip_adress):
    with session() as new_session:
        query = select(ChatRequest).filter_by(ip_address=ip_adress)
        result = new_session.execute(query)
        return result.scalars().all()

