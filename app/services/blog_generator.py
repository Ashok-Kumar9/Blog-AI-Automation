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
CURRENT TASK: LONG-FORM AUTHORITY BLOG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Topic          : [{topic}]
Target audience: [{audience}]
Word count goal: [{word_count}+ words — write with depth, ensure no fluff]
Specific goal  : [{specific_goal}]
INTERNAL LINKS:  [{links_formatted}]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. GENERIC CONTENT GENERATION PROCESS (MANDATORY)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Follow this structured approach for any content:

Step 1: Understand Context
- Identify target audience (persona), intent, and goal of content
- Identify whether content is educational, informational, or decision-support

Step 2: Generate SEO Metadata
- SEO URL (clean and keyword-focused)
- SEO Title (clear, relevant, benefit-led)
- SEO Description (concise, informative, user-focused)

Step 3: Create Title
- Use Title Case
- Ensure clarity and relevance to audience need

Step 4: Write Introduction
- Start with a relatable situation, challenge, or aspiration
- Establish relevance to the target audience
- Set context clearly

Step 5: Develop Main Content Sections
- Break content into logical sections with clear headings
- Maintain flow: awareness → understanding → solutions → action
- Keep paragraphs concise and easy to read

Step 6: Explain Key Concepts
- Simplify financial or technical terms where needed
- Provide short explanations for first-time users

Step 7: Provide Solutions or Options
- Present available approaches, schemes, or strategies
- Use structured formatting (lists, bullets, sections)

Step 8: Integrate Credit Saison India Offerings
- Introduce products naturally within context
- Map product to user need or scenario
- Focus on usefulness, not promotion

Step 9: Add Practical Guidance
- Include actionable tips, best practices, or considerations
- Ensure advice is realistic and applicable

Step 10: Build Trust
- Reinforce reliability through transparency, clarity, and user benefit
- Avoid exaggerated claims

Step 11: Summarise Key Points
- Provide a concise recap using bullet points

Step 12: Write Conclusion
- Reinforce confidence and clarity
- Align with emotional goal (support, hope, empowerment)

Step 13: Add Soft Call-To-Action
- Encourage next steps naturally
- Avoid pressure or urgency tactics

Step 14: Optional Product Summary Section
- List relevant solutions if applicable
- Keep it clean and benefit-oriented

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. OUTPUT QUALITY CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Before finalising, ensure:
- Content is relevant to the intended audience
- Tone is human, clear, and supportive
- No aggressive or sales-driven language
- Terminology is explained where needed
- Structure is logical and easy to follow
- Product mentions are contextual and helpful
- No em dash used anywhere
"""


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
        tools=[{"type": "web_search_preview"}],
        max_tokens=6000,
    )

    return response.choices[0].message.content.strip()