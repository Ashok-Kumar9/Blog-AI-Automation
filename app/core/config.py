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
    
    # Default Topics Generation
    DEFAULT_BLOG_CATEGORY: str = "MSME Loan"
    DEFAULT_COMPETITORS: List[str] = ["Bajaj Finserv", "Lendingkart", "Tata Capital"]
    
    # Default Blog Generation
    DEFAULT_TARGET_AUDIENCE: str = "Small business owners and entrepreneurs in Tier 2 and Tier 3 cities"
    DEFAULT_WORD_COUNT_GOAL: int = 2500
    DEFAULT_SPECIFIC_GOAL: str = "Encourage female entrepreneurs to explore expansion loans for their businesses"
    DEFAULT_INTERNAL_LINKS: List[str] = [
        "https://creditsaison.in/business-loan",
        "https://creditsaison.in/vyapari-loans",
        "https://creditsaison.in/home-loan",
        "https://creditsaison.in/doctor-loan",
        "https://creditsaison.in/small-business-loan",
        "https://creditsaison.in/loan-against-property",
    ]

settings = Settings()
