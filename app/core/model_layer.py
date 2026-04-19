from functools import lru_cache
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

OPENAI_TEXT_MODEL  = "gpt-4o"
OPENAI_IMAGE_MODEL = "gpt-image-1.5"
GEMINI_TEXT_MODEL  = "gemini-2.5-flash"
GEMINI_IMAGE_MODEL = "gemini-2.5-flash-image"


class AIProvider:
    """
    Singleton AI provider supporting OpenAI and Gemini.
    All text calls use web search grounding. Clients are lazy-loaded.

    Usage:
        provider.generate(user_prompt, system_prompt)   # text
        provider.generate_image(prompt)                 # image
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._clients: dict = {}
        self._provider = settings.AI_PROVIDER.lower()
        self._initialized = True
        logger.info(f"AIProvider initialized | provider={self._provider}")

    # ── Lazy clients ──────────────────────────────────────────────────────────

    @property
    def _openai_client(self):
        if "openai" not in self._clients:
            import httpx
            from openai import OpenAI
            self._clients["openai"] = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                http_client=httpx.Client(verify=False),
            )
        return self._clients["openai"]

    @property
    def _gemini_client(self):
        if "gemini" not in self._clients:
            from google import genai
            self._clients["gemini"] = genai.Client(api_key=settings.GEMINI_API_KEY)
        return self._clients["gemini"]

    # ── Public API ────────────────────────────────────────────────────────────

    def generate(self, user_prompt: str, system_prompt: str = "") -> str:
        if self._provider == "openai":
            return self._openai_text(system_prompt, user_prompt)
        return self._gemini_text(system_prompt, user_prompt)

    def generate_image(self, prompt: str) -> bytes:
        if self._provider == "openai":
            return self._openai_image(prompt)
        return self._gemini_image(prompt)

    # ── OpenAI ────────────────────────────────────────────────────────────────

    def _openai_text(self, system_prompt: str, user_prompt: str) -> str:
        input_content = (
            [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
            if system_prompt else user_prompt
        )
        return self._openai_client.responses.create(
            model=OPENAI_TEXT_MODEL,
            tools=[{"type": "web_search_preview"}],
            input=input_content,
        ).output_text.strip()

    def _openai_image(self, prompt: str) -> bytes:
        import base64
        response = self._openai_client.images.generate(
            model=OPENAI_IMAGE_MODEL, prompt=prompt,
            size="1536x1024", quality="medium",
            output_format="png", n=1,
        )
        b64 = response.data[0].b64_json
        if not b64:
            raise ValueError("OpenAI image generation returned no data.")
        return base64.b64decode(b64)

    # ── Gemini ────────────────────────────────────────────────────────────────

    def _gemini_text(self, system_prompt: str, user_prompt: str) -> str:
        from google.genai import types
        config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            **({"system_instruction": system_prompt} if system_prompt else {}),
        )
        return self._gemini_client.models.generate_content(
            model=GEMINI_TEXT_MODEL,
            contents=user_prompt,
            config=config,
        ).text.strip()

    def _gemini_image(self, prompt: str) -> bytes:
        from google.genai import types
        response = self._gemini_client.models.generate_content(
            model=GEMINI_IMAGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                return part.inline_data.data
        raise ValueError("Gemini image generation returned no image data.")

    def __repr__(self) -> str:
        return f"<AIProvider provider={self._provider} cached={list(self._clients)}>"


@lru_cache()
def get_provider() -> AIProvider:
    return AIProvider()


provider = get_provider()
