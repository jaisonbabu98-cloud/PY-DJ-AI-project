from google import genai
from google.genai import types
from django.conf import settings

class LLMError(Exception):
    pass

_client = None

def _get_client():
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            raise LLMError("GEMINI_API_KEY is not configured in .env")
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client

def generate_text(system_prompt, messages, max_tokens=1500):
    client = _get_client()
    user_content = messages[-1]["content"] if messages else ""

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=user_content,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=max_tokens,
                temperature=0.7,
            ),
        )
        return response.text
    except Exception as exc:
        raise LLMError(str(exc)) from exc