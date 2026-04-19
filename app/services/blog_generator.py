from typing import List
from dataclasses import dataclass
from app.core.model_layer import provider
from app.services.prompts import SYSTEM_PROMPT


@dataclass
class InternalLink:
    product_keyword: str
    url: str
    integration_count: int


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
    user_prompt = build_user_prompt(topic, audience, word_count, specific_goal, internal_links)
    return provider.generate(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)