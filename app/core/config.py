import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Settings
    APP_TITLE: str = "Blog Automation AI"
    APP_VERSION: str = "1.0.0"
    
    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    


settings = Settings()
