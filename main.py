from contextlib import asynccontextmanager

from fastapi import FastAPI, Body, Request

from db import Base, engine, get_user_requests

from gemini_client import get_answer_from_gemini

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("Все таблицы созданы")
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/request")
def get_my_request(requst: Request):
    user_ip_address = request.client.host
    print(f"{user_ip_address}")
    user_request = get_user_requests(ip_adress=user_ip_adress)
    return "Hello World"


@app.post("/request")
def send_prompt(
        prompt: str = Body(embed=True)
):
    answer = get_answer_from_gemini(prompt)
    return {"answer": answer}