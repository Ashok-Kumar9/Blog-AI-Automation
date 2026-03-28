from typing import List
from app.core.openai_utils import client

def generate_trending_topics(category: str, competitors: List[str]) -> List[str]:
    """Generates 10 SEO-friendly blog post titles using OpenAI's web search tool."""
    
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
