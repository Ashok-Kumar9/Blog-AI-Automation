import os
import json
import httpx
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=httpx.Client(verify=False),
)

BLOG_CATEGORY = "MSME Loan"
COMPETITORS = ["Bajaj Finserv", "Lendingkart", "Tata Capital"]


def generate_trending_topics(category: str, competitors: list) -> list[str]:

    prompt = f"""You are an expert SEO content strategist for fintech and business loans.

Use Google Search to analyze recent blog content from these competitors: {competitors}

Then generate exactly 10 high-quality, SEO-friendly blog post titles for the category: "{category}".

Guidelines:
- Search competitor sites to identify what topics they already cover well, then avoid those
- Focus on content gaps — topics competitors have missed or covered poorly
- Target high-intent users who are likely to apply for a loan
- Prioritize the Indian market: MSMEs, startups, self-employed professionals, small business owners
- Titles must be specific, clear, and clickable — not generic
- Avoid basic explainer topics like "What is a Business Loan"
- Prefer action-oriented or problem-solving angles (e.g., "how to get", "best options for", "mistakes to avoid")

Output format (strict):
- A numbered list of exactly 10 titles
- No explanations, headings, or extra text
- Only the list"""

    response = client.responses.create(
        model="gpt-4o-mini",
        tools=[{"type": "web_search_preview"}],
        input=prompt,
    )

    raw = response.output_text.strip()
    topics = [
        line.lstrip("0123456789.-) ").strip()
        for line in raw.splitlines()
        if line.strip() and line.strip()[0].isdigit()
    ]
    return topics


def save_output(topics: list[str], category: str):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/{category.replace(' ', '_').lower()}_{timestamp}.json"

    data = {
        "category": category,
        "competitors": COMPETITORS,
        "generated_at": datetime.now().isoformat(),
        "topics": topics,
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Output saved to: {filename}")
    return filename


def run():
    print(f"\nAnalyzing '{BLOG_CATEGORY}' against {len(COMPETITORS)} competitors...")
    topics = generate_trending_topics(BLOG_CATEGORY, COMPETITORS)
    save_output(topics, BLOG_CATEGORY)
    return topics


if __name__ == "__main__":
    run()