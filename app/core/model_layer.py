from functools import lru_cache
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

GEMINI_BLOG_MODEL   = "gemini-2.5-flash"
GEMINI_IMAGE_MODEL  = "gemini-2.5-flash-image"
GEMINI_IMAGEN_MODEL = "imagen-4.0-generate-001"
OPENAI_TITLE_MODEL  = "gpt-4o"


class GeminiClient:
    """
    Gemini sub-client.

    Usage:
        llm_provider.gemini.generate_blog(user_prompt, system_prompt)
        llm_provider.gemini.generate_image(prompt)
    """

    def __init__(self):
        self._client = None

    @property
    def _sdk(self):
        if self._client is None:
            from google import genai
            self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
            logger.debug("Gemini SDK client initialized")
        return self._client

    def generate(self, user_prompt: str, system_prompt: str = "") -> str:
        from google.genai import types
        config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            **({"system_instruction": system_prompt} if system_prompt else {}),
        )
        return self._sdk.models.generate_content(
            model=GEMINI_BLOG_MODEL,
            contents=user_prompt,
            config=config,
        ).text.strip()

    def generate_image(self, prompt: str) -> bytes:
        from google.genai import types
        response = self._sdk.models.generate_content(
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

    def generate_image_imagen(self, prompt: str, number_of_images: int = 1) -> list[bytes]:
        from google.genai import types
        response = self._sdk.models.generate_images(
            model=GEMINI_IMAGEN_MODEL,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=number_of_images,
            ),
        )
        images = [gi.image.image_bytes for gi in response.generated_images]
        if not images:
            raise ValueError("Imagen returned no image data.")
        return images

    def __repr__(self) -> str:
        return f"<GeminiClient initialized={self._client is not None}>"


class OpenAIClient:
    """
    OpenAI sub-client.

    Usage:
        llm_provider.openai.generate_title(user_prompt)
    """

    def __init__(self):
        self._client = None

    @property
    def _sdk(self):
        if self._client is None:
            import httpx
            from openai import OpenAI
            self._client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                http_client=httpx.Client(verify=False),
            )
            logger.debug("OpenAI SDK client initialized")
        return self._client

    def generate(self, user_prompt: str) -> str:
        return self._sdk.responses.create(
            model=OPENAI_TITLE_MODEL,
            tools=[{"type": "web_search_preview"}],
            input=user_prompt,
        ).output_text.strip()

    def __repr__(self) -> str:
        return f"<OpenAIClient initialized={self._client is not None}>"


class LLMProvider:
    """
    Singleton provider exposing Gemini and OpenAI sub-clients.

    Usage:
        llm_provider.gemini.generate_blog(user_prompt, system_prompt)
        llm_provider.gemini.generate_image(prompt)
        llm_provider.openai.generate_title(user_prompt)
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
        self.gemini = GeminiClient()
        self.openai = OpenAIClient()
        self._initialized = True
        logger.info("LLMProvider initialized")

    def __repr__(self) -> str:
        return f"<LLMProvider gemini={self.gemini} openai={self.openai}>"


@lru_cache()
def get_provider() -> LLMProvider:
    return LLMProvider()


llm_provider = get_provider()
