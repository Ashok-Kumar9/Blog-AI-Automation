from typing import List
from dataclasses import dataclass
from app.core.openai_utils import client


@dataclass
class InternalLink:
    product_keyword: str   # Anchor text / keyword to link from
    url: str               # Destination URL
    integration_count: int # How many times it should appear in the article


from app.services.prompts import SYSTEM_PROMPT


def _format_internal_links(internal_links: List[InternalLink]) -> str:
    lines = []
    for i, link in enumerate(internal_links, start=1):
        lines.append(
            f"  {i}. Keyword : \"{link.product_keyword}\"\n"
            f"     URL     : {link.url}\n"
            f"     Embed   : exactly {link.integration_count} time(s) across the article"
        )
    return "\n\n".join(lines)


def build_user_prompt(
    topic: str,
    audience: str,
    word_count: int,
    specific_goal: str,
    internal_links: List[InternalLink],
) -> str:
    links_formatted = _format_internal_links(internal_links)

    return f"""\
Topic: [{topic}]
Target Audience: [{audience}]
Content Goal: [{specific_goal}]
Word Count Target: [{word_count}+ words]

Internal Links:
[{links_formatted}]
- Integrate naturally within relevant sections only
""".strip()


def generate_blog(
    topic: str,
    audience: str,
    word_count: int,
    specific_goal: str,
    internal_links: List[InternalLink],
) -> str:
    """Generates a full blog post using OpenAI's gpt-4o model with web search."""
    user_prompt = build_user_prompt(topic, audience, word_count, specific_goal, internal_links)

    response = client.responses.create(
        model="gpt-4o",
        tools=[{"type": "web_search_preview"}],
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        max_output_tokens=6000,
    )

    return response.output_text.strip()