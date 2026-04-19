from typing import List
from app.core.model_layer import provider

def generate_trending_topics(category: str) -> List[str]:
    """Generates 10 SEO-friendly blog post titles using OpenAI's web search tool."""
    
    prompt = f"""
You are an expert SEO content strategist specializing in the Indian BFSI (Banking, Financial Services & Insurance) sector, with deep knowledge of lending products, NBFC regulations, and the financial needs of MSMEs, startups, and self-employed professionals in India.

Use Google Search to analyze recent blog and article content published by leading Indian NBFCs (such as Bajaj Finserv, Lendingkart, NeoGrowth, Flexi Loans, Ugro Capital, Indifi, Kinara Capital) and major BFSI publishers (such as BankBazaar, Paisabazaar, Moneycontrol, Economic Times BFSI, Financial Express).

Then generate exactly 10 high-quality, SEO-friendly blog post titles for the category: "{category}".

Guidelines:
- Search NBFC and BFSI websites to identify topics they already cover well, then avoid those
- Focus on content gaps — angles, audiences, or pain points that are underserved or missing
- Target high-intent users who are actively researching or ready to apply for a loan
- Prioritize the Indian market: MSMEs, startups, self-employed professionals, small business owners, and new-to-credit borrowers
- Titles must be specific, clear, and clickable — not generic or introductory
- Avoid basic explainer topics like "What is a Business Loan" or "Types of Business Loans"
- Prefer action-oriented or problem-solving angles (e.g., "how to get", "best options for", "mistakes to avoid", "what lenders won't tell you")
- Incorporate relevant Indian context where appropriate (GST, ITR, CIBIL, MSME registration, Udyam, etc.)

Output format (strict):
- A numbered list of exactly 10 titles
- No explanations, headings, or extra text
- Only the list
""".strip()

    raw = provider.generate_topics(user_prompt=prompt)
    topics = [
        line.lstrip("0123456789.-) ").strip().strip('"')
        for line in raw.splitlines()
        if line.strip() and line.strip()[0].isdigit()
    ]
    return topics
