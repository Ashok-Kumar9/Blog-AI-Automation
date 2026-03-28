import httpx
from openai import OpenAI
from app.core.config import settings

def get_openai_client() -> OpenAI:
    """Provides a shared OpenAI client with custom configuration."""
    return OpenAI(
        api_key=settings.OPENAI_API_KEY,
        http_client=httpx.Client(verify=False),
    )

client = get_openai_client()
