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
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK: GENERATE A LONG-FORM AUTHORITY BLOG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Using the details below, generate a complete blog by strictly following BOTH:
1. The system prompt guidelines
2. The exact output format defined below

Topic: [{topic}]
Target Audience: [{audience}]
Content Goal: [{specific_goal}]
Word Count Target: [{word_count}+ words]

Internal Links:
[{links_formatted}]
- Integrate naturally within relevant sections only

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT OUTPUT FORMAT (DO NOT DEVIATE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You MUST follow this exact structure, headings, and markdown format:

# SEO Meta Tags

* **SEO URL:** <value>
* **SEO Title:** <value>
* **SEO Description:** <value>

---

# <Blog Title in Title Case>

<Introduction section - no heading label "Introduction">

## <First Section Heading>

<Content>

## <Next Section Heading>

<Content>

## <Next Section Heading>

<Content>

(Continue structured sections as needed)

## Tips / Practical Guidance Section

<Use numbered or structured format>

## <Optional Supporting Section if needed>

<Content>

## Why Choose Credit Saison India?

<Trust-building section with sub-points if needed>

## Key Takeaways

1. <Point>
2. <Point>
3. <Point>

## Conclusion: <Title Case Ending>

<Conclusion content>

---

### Explore Our Solutions:
* [<CTA 1>](<link>)
* [<CTA 2>](<link>)
* [<CTA 3>](<link>)
(Include only relevant links)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WORD COUNT ENFORCEMENT (MANDATORY)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- The blog MUST be at least [{word_count}] words
- This is an authority-level blog, not a summary
- Do NOT stop early even if topic feels complete
- Expand with depth, not repetition

Section-wise expansion guidance:
- Introduction: 150–250 words
- Each main section: 250–400 words
- Tips section: 300–500 words
- Why Choose section: 200–300 words
- Conclusion: 150–200 words

If content is short, expand using:
- Examples
- Use cases
- Explanations
- Sub-sections where relevant

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SELF-CHECK BEFORE FINAL OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Before finishing:
- Estimate total word count
- If below [{word_count}], expand weakest sections
- Ensure no fluff or repetition
- Only then return final answer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMPORTANT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Do NOT rename sections (e.g., do NOT write "SEO Metadata")
- Do NOT add extra headings like "Introduction"
- Do NOT change markdown structure
- Use --- separators exactly as shown
- Ensure consistent formatting across the blog
- Follow all brand, tone, and writing guidelines from system prompt
""".strip()


def generate_blog(
    topic: str,
    audience: str,
    word_count: int,
    specific_goal: str,
    internal_links: List[InternalLink],
) -> str:
    """Generates a full blog post using OpenAI's gpt-4o model."""
    user_prompt = build_user_prompt(topic, audience, word_count, specific_goal, internal_links)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        # tools=[{"type": "web_search_preview"}],
        max_tokens=6000,
    )

    return response.choices[0].message.content.strip()