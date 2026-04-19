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


settings = Settings()
