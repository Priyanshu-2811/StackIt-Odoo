import httpx
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def get_ai_answer(question_text: str):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            params={"key": GEMINI_API_KEY},
            json={"contents": [{"parts": [{"text": question_text}]}]}
        )
    return res.json()