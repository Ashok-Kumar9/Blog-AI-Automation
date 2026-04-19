from functools import lru_cache
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

MODEL_REGISTRY = {
    "blog": {
        "openai": {"model": "gpt-4o",          "max_tokens": 6000, "web_search": True},
        "gemini": {"model": "gemini-2.0-flash", "max_tokens": 6000, "web_search": True},
    },
    "topic": {
        "openai": {"model": "gpt-4o-mini",      "max_tokens": None, "web_search": True},
        "gemini": {"model": "gemini-2.0-flash", "max_tokens": None, "web_search": True},
    },
    "image": {
        "openai": {"model": "gpt-image-1.5", "size": "1536x1024", "quality": "medium", "format": "png"},
        "gemini": {"model": "imagen-3.0-generate-002", "aspect_ratio": "16:9",
                   "safety_filter_level": "block_some", "person_generation": "allow_adult"},
    },
}


class AIProvider:
    """
    Singleton AI provider supporting OpenAI and Gemini.
    Clients are lazy-loaded and cached on first use.

    Usage:
        provider.generate("blog", user_prompt, system_prompt)
        provider.generate("topic", user_prompt)
        provider.generate("image", prompt)
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

    def generate(self, task: str, user_prompt: str, system_prompt: str = "") -> str | bytes:
        cfg = MODEL_REGISTRY[task][self._provider]
        if task == "image":
            return self._image_call(user_prompt, cfg)
        return self._text_call(system_prompt, user_prompt, cfg)

    # ── Internal dispatch ─────────────────────────────────────────────────────

    def _text_call(self, system_prompt: str, user_prompt: str, cfg: dict) -> str:
        if self._provider == "openai":
            return self._openai_text(system_prompt, user_prompt, cfg)
        return self._gemini_text(system_prompt, user_prompt, cfg)

    def _image_call(self, prompt: str, cfg: dict) -> bytes:
        if self._provider == "openai":
            return self._openai_image(prompt, cfg)
        return self._gemini_image(prompt, cfg)

    # ── OpenAI ────────────────────────────────────────────────────────────────

    def _openai_text(self, system_prompt: str, user_prompt: str, cfg: dict) -> str:
        tools = [{"type": "web_search_preview"}] if cfg["web_search"] else []
        input_content = (
            [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
            if system_prompt else user_prompt
        )
        kwargs: dict = dict(model=cfg["model"], tools=tools, input=input_content)
        if cfg["max_tokens"]:
            kwargs["max_output_tokens"] = cfg["max_tokens"]
        return self._openai_client.responses.create(**kwargs).output_text.strip()

    def _openai_image(self, prompt: str, cfg: dict) -> bytes:
        import base64
        response = self._openai_client.images.generate(
            model=cfg["model"], prompt=prompt,
            size=cfg["size"], quality=cfg["quality"],
            output_format=cfg["format"], n=1,
        )
        b64 = response.data[0].b64_json
        if not b64:
            raise ValueError("OpenAI image generation returned no data.")
        return base64.b64decode(b64)

    # ── Gemini ────────────────────────────────────────────────────────────────

    def _gemini_text(self, system_prompt: str, user_prompt: str, cfg: dict) -> str:
        from google.genai import types
        config_kwargs: dict = {}
        if system_prompt:
            config_kwargs["system_instruction"] = system_prompt
        if cfg["max_tokens"]:
            config_kwargs["max_output_tokens"] = cfg["max_tokens"]
        if cfg["web_search"]:
            config_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]
        response = self._gemini_client.models.generate_content(
            model=cfg["model"],
            contents=user_prompt,
            config=types.GenerateContentConfig(**config_kwargs) if config_kwargs else None,
        )
        return response.text.strip()

    def _gemini_image(self, prompt: str, cfg: dict) -> bytes:
        from google.genai import types
        response = self._gemini_client.models.generate_images(
            model=cfg["model"],
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=cfg["aspect_ratio"],
                safety_filter_level=cfg["safety_filter_level"],
                person_generation=cfg["person_generation"],
            ),
        )
        return response.generated_images[0].image.image_bytes

    def __repr__(self) -> str:
        return f"<AIProvider provider={self._provider} cached={list(self._clients)}>"


@lru_cache()
def get_provider() -> AIProvider:
    return AIProvider()


provider = get_provider()
