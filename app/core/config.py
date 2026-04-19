import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_TITLE: str = "Blog Automation AI"
    APP_VERSION: str = "1.0.0"

    # ── Provider selection ────────────────────────────────────────────────────
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai")  # "openai" | "gemini"

    # ── API keys ──────────────────────────────────────────────────────────────
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # ── OpenAI models ─────────────────────────────────────────────────────────
    OPENAI_BLOG_MODEL:  str = os.getenv("OPENAI_BLOG_MODEL",  "gpt-4o")
    OPENAI_TOPIC_MODEL: str = os.getenv("OPENAI_TOPIC_MODEL", "gpt-4o-mini")
    OPENAI_IMAGE_MODEL: str = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1.5")

    # ── Gemini models ─────────────────────────────────────────────────────────
    GEMINI_BLOG_MODEL:  str = os.getenv("GEMINI_BLOG_MODEL",  "gemini-2.0-flash")
    GEMINI_TOPIC_MODEL: str = os.getenv("GEMINI_TOPIC_MODEL", "gemini-2.0-flash")
    GEMINI_IMAGE_MODEL: str = os.getenv("GEMINI_IMAGE_MODEL", "imagen-3.0-generate-002")


settings = Settings()
