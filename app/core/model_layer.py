from abc import ABC, abstractmethod
from app.core.config import settings

MODEL_REGISTRY: dict = {
    "openai": {
        "blog":  {"model": "gpt-4o",      "max_tokens": 6000, "web_search": True},
        "topic": {"model": "gpt-4o-mini",  "max_tokens": None, "web_search": True},
        "image": {"model": "gpt-image-1.5", "size": "1536x1024", "quality": "medium", "format": "png"},
    },
    "gemini": {
        "blog":  {"model": "gemini-2.0-flash", "max_tokens": 6000, "web_search": True},
        "topic": {"model": "gemini-2.0-flash", "max_tokens": None, "web_search": True},
        "image": {"model": "imagen-3.0-generate-002", "aspect_ratio": "16:9",
                  "safety_filter_level": "block_some", "person_generation": "allow_adult"},
    },
}


class AIProvider(ABC):
    def __init__(self, provider_name: str) -> None:
        self._cfg = MODEL_REGISTRY[provider_name]

    def generate_blog(self, system_prompt: str, user_prompt: str) -> str:
        return self._text_call(system_prompt, user_prompt, self._cfg["blog"])

    def generate_topics(self, user_prompt: str) -> str:
        return self._text_call("", user_prompt, self._cfg["topic"])

    def generate_image(self, prompt: str) -> bytes:
        return self._image_call(prompt, self._cfg["image"])

    @abstractmethod
    def _text_call(self, system_prompt: str, user_prompt: str, cfg: dict) -> str: ...

    @abstractmethod
    def _image_call(self, prompt: str, cfg: dict) -> bytes: ...


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
            model=cfg["model"], prompt=prompt,
            size=cfg["size"], quality=cfg["quality"],
            output_format=cfg["format"], n=1,
        )
        b64 = response.data[0].b64_json
        if not b64:
            raise ValueError("OpenAI image generation returned no data.")
        return base64.b64decode(b64)


class GeminiProvider(AIProvider):
    def __init__(self, api_key: str) -> None:
        super().__init__("gemini")
        from google import genai
        self._client = genai.Client(api_key=api_key)
        self._genai = genai

    def _text_call(self, system_prompt: str, user_prompt: str, cfg: dict) -> str:
        from google.genai import types
        config_kwargs: dict = {}
        if system_prompt:
            config_kwargs["system_instruction"] = system_prompt
        if cfg["max_tokens"]:
            config_kwargs["max_output_tokens"] = cfg["max_tokens"]
        if cfg["web_search"]:
            config_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]
        response = self._client.models.generate_content(
            model=cfg["model"],
            contents=user_prompt,
            config=types.GenerateContentConfig(**config_kwargs) if config_kwargs else None,
        )
        return response.text.strip()

    def _image_call(self, prompt: str, cfg: dict) -> bytes:
        from google.genai import types
        response = self._client.models.generate_images(
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


def get_provider() -> AIProvider:
    if settings.AI_PROVIDER.lower() == "gemini":
        return GeminiProvider(api_key=settings.GEMINI_API_KEY)
    return OpenAIProvider(api_key=settings.OPENAI_API_KEY)


provider = get_provider()
