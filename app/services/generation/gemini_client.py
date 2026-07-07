# pyrefly: ignore [missing-import]
from google import genai

from app.core.config import GEMINI_API_KEY


client = None
if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


def generate_response(prompt: str):
    if not client:
        raise ValueError("GEMINI_API_KEY is not configured. Cannot generate response.")

    # Send prompt to Gemini model
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
