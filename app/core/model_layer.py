from abc import ABC, abstractmethod
from typing import Optional

from app.core.config import settings

# ─── Central Model Registry ────────────────────────────────────────────────────
# Model names come from settings/env — nothing hardcoded here.
# To swap a model, set the corresponding env var in .env (see config.py).
MODEL_REGISTRY: dict = {
    "openai": {
        "blog":  {"model": settings.OPENAI_BLOG_MODEL,  "max_tokens": 6000, "web_search": True},
        "topic": {"model": settings.OPENAI_TOPIC_MODEL, "max_tokens": None, "web_search": True},
        "image": {"model": settings.OPENAI_IMAGE_MODEL, "size": "1536x1024", "quality": "medium", "format": "png"},
    },
    "gemini": {
        "blog":  {"model": settings.GEMINI_BLOG_MODEL,  "max_tokens": 6000, "web_search": True},
        "topic": {"model": settings.GEMINI_TOPIC_MODEL, "max_tokens": None, "web_search": True},
        "image": {"model": settings.GEMINI_IMAGE_MODEL, "aspect_ratio": "16:9",
                  "safety_filter_level": "block_some", "person_generation": "allow_adult"},
    },
}
# ──────────────────────────────────────────────────────────────────────────────


class AIProvider(ABC):
    """Base provider. Subclasses implement _text_call and _image_call only."""

    def __init__(self, provider_name: str) -> None:
        self._provider_name = provider_name
        self._cfg = MODEL_REGISTRY[provider_name]
        print(f"[AI] Provider: {provider_name.upper()} | "
              f"blog={self._cfg['blog']['model']} | "
              f"topic={self._cfg['topic']['model']} | "
              f"image={self._cfg['image']['model']}", flush=True)

    # ── Public task API (used by services) ────────────────────────────────────

    def generate_blog(self, system_prompt: str, user_prompt: str) -> str:
        print(f"[AI] generate_blog  → {self._cfg['blog']['model']}", flush=True)
        return self._text_call(system_prompt, user_prompt, self._cfg["blog"])

    def generate_topics(self, user_prompt: str) -> str:
        print(f"[AI] generate_topics → {self._cfg['topic']['model']}", flush=True)
        return self._text_call("", user_prompt, self._cfg["topic"])

    def generate_image(self, prompt: str) -> bytes:
        print(f"[AI] generate_image  → {self._cfg['image']['model']}", flush=True)
        return self._image_call(prompt, self._cfg["image"])

    # ── SDK-level hooks (implemented per provider) ────────────────────────────

    @abstractmethod
    def _text_call(self, system_prompt: str, user_prompt: str, cfg: dict) -> str: ...

    @abstractmethod
    def _image_call(self, prompt: str, cfg: dict) -> bytes: ...


# ─── OpenAI ───────────────────────────────────────────────────────────────────

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str) -> None:
        super().__init__("openai")
        import httpx
        from openai import OpenAI
        self._client = OpenAI(api_key=api_key, http_client=httpx.Client(verify=False))

    def _text_call(self, system_prompt: str, user_prompt: str, cfg: dict) -> str:
        tools = [{"type": "web_search_preview"}] if cfg["web_search"] else []
        input_content = (
            [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
            if system_prompt else user_prompt
        )
        kwargs: dict = dict(model=cfg["model"], tools=tools, input=input_content)
        if cfg["max_tokens"]:
            kwargs["max_output_tokens"] = cfg["max_tokens"]
        return self._client.responses.create(**kwargs).output_text.strip()

    def _image_call(self, prompt: str, cfg: dict) -> bytes:
        import base64
        response = self._client.images.generate(
            model=cfg["model"],
            prompt=prompt,
            size=cfg["size"],
            quality=cfg["quality"],
            output_format=cfg["format"],
            n=1,
        )
        b64 = response.data[0].b64_json
        if not b64:
            raise ValueError("OpenAI image generation returned no data.")
        return base64.b64decode(b64)


# ─── Gemini ───────────────────────────────────────────────────────────────────

class GeminiProvider(AIProvider):
    def __init__(self, api_key: str) -> None:
        super().__init__("gemini")
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self._genai = genai

    def _text_call(self, system_prompt: str, user_prompt: str, cfg: dict) -> str:
        genai = self._genai
        tools = (
            [genai.protos.Tool(google_search_retrieval=genai.protos.GoogleSearchRetrieval())]
            if cfg["web_search"] else []
        )
        model = genai.GenerativeModel(
            model_name=cfg["model"],
            system_instruction=system_prompt or None,
            tools=tools or None,
        )
        gen_config = {"max_output_tokens": cfg["max_tokens"]} if cfg["max_tokens"] else None
        return model.generate_content(user_prompt, generation_config=gen_config).text.strip()

    def _image_call(self, prompt: str, cfg: dict) -> bytes:
        genai = self._genai
        model = genai.ImageGenerationModel(cfg["model"])
        response = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio=cfg["aspect_ratio"],
            safety_filter_level=cfg["safety_filter_level"],
            person_generation=cfg["person_generation"],
        )
        return response.images[0]._image_bytes


# ─── Factory ──────────────────────────────────────────────────────────────────

def get_provider() -> AIProvider:
    if settings.AI_PROVIDER.lower() == "gemini":
        return GeminiProvider(api_key=settings.GEMINI_API_KEY)
    return OpenAIProvider(api_key=settings.OPENAI_API_KEY)


provider = get_provider()
