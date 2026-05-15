import google.generativeai as genai

from app.config import GEMINI_API_KEY


genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)


def get_answer_from_gemini(messages):

    prompt = ""

    for message in messages:

        prompt += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    response = model.generate_content(
        prompt
    )

    return response.text