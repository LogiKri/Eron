from groq import AsyncGroq

from app.config import config

DEFAULT_MODEL = "llama-3.3-70b-versatile"


class LLMNotConfigured(RuntimeError):
    pass


def _client() -> AsyncGroq:
    if not config.groq_token:
        raise LLMNotConfigured("GROQ_TOKEN is not set in .env")
    return AsyncGroq(api_key=config.groq_token)


async def chat_completion(system_role: str, history: list[dict[str, str]], model: str = DEFAULT_MODEL) -> str:
    client = _client()
    messages = [{"role": "system", "content": system_role}, *history]

    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1024,
    )
    return response.choices[0].message.content
