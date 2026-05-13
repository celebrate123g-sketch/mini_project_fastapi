from contextlib import asynccontextmanager

from fastapi import FastAPI, Body, Request

from db import (
    Base,
    engine,
    get_user_requests,
    add_request_data
)

from gemini_client import get_answer_from_gemini


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Все таблицы созданы")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"status": "working"}


@app.get("/request")
def get_requests(request: Request):

    user_ip_address = request.client.host

    requests = get_user_requests(
        ip_address=user_ip_address
    )

    return {
        "ip_address": user_ip_address,
        "requests": requests
    }


@app.post("/request")
def send_prompt(
        request: Request,
        prompt: str = Body(embed=True)
):

    user_ip_address = request.client.host

    answer = get_answer_from_gemini(prompt)

    add_request_data(
        ip_address=user_ip_address,
        prompt=prompt,
        answer=answer
    )

    return {
        "answer": answer
    }