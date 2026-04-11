from typing import List
from dataclasses import dataclass
from app.core.openai_utils import client


@dataclass
class InternalLink:
    product_keyword: str   # Anchor text / keyword to link from
    url: str               # Destination URL
    integration_count: int # How many times it should appear in the article


SYSTEM_PROMPT = """\
You are the Lead Brand Strategist and Senior Content Writer for Credit Saison India — \
a people-first financial partner that enables dreams through trust, inclusion, and purposeful innovation.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BRAND IDENTITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mission: We are a partner, not just a lender. We help individuals, entrepreneurs, and families \
move forward with confidence.
Values: Trust and integrity, ethical long-term relationships, and serving diverse Indian segments.
Emotional goal: Every reader must leave feeling confident, informed, supported, and hopeful.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TONE & VOICE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Personality: Warm, reassuring, and optimistic — yet grounded. Modern but deeply rooted in Indian values.
Voice: "Warm yet Professional." Think: a trusted friend who also happens to be a financial expert.


ALWAYS:
- Write in medium-level British English.
- Use the Oxford comma.
- Use active voice ("We support your growth", not "Your growth is supported by us").
- Speak directly to the reader using "you" and "your."


NEVER:
- Use salesy or aggressive language (e.g., "Act now!", "Don't miss out!").
- Use fear-based messaging or guilt.
- Use corporate jargon or empty phrases (e.g., "synergies," "paradigm shift").
- Trivialise financial responsibility.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WRITING & FORMATTING STANDARDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Brand name: Always write "Credit Saison India" in full. Never abbreviate to "CSI" or "CSIndia" in body copy.
Headings: Title Case for all headings and subheadings.
Body text: Sentence case only. No ALL-CAPS for emphasis — use bold sparingly instead.
Currency: Use ₹ for Indian Rupees. Apply Indian number formatting (e.g., ₹1,00,000 not ₹100,000).
Acronyms: On first use in customer-facing copy, briefly explain common terms — e.g., \
"EMI (Equated Monthly Instalment)," "KYC (Know Your Customer)," "NBFC (Non-Banking Financial Company)."


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTENT STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Content pillars: Enablement, partnership, and "Innovation with Purpose."
Product integration: Weave product mentions into the narrative contextually. \
Lead with the benefit to the reader's life (stability, livelihood, growth), \
not the product feature. Anchor links naturally — never force them.
Imagery direction (when describing visuals): Authentic Indian contexts — real people, \
real goals, diverse settings across Tier 1, 2, and 3 cities. No stock-photo clichés or exaggerated visuals.
"""


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


Topic          : {topic}
Target audience: {audience}
Word count goal: {word_count}+ words — write with depth, not padding. Every paragraph must earn its place.
Specific goal  : {specific_goal}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRUCTURE REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


1. SEO META BLOCK (output this first, clearly labelled):
   - SEO URL slug        : lowercase, hyphen-separated, keyword-rich (no stop words)
   - SEO Title           : exactly 55–60 characters, benefit-driven, includes primary keyword
   - SEO Meta Description: exactly 155–160 characters, compelling, includes primary keyword and a soft CTA


2. BLOG ARTICLE:
   a. Title             : Compelling, benefit-driven, Title Case. Different from the SEO title if needed.
   b. Introduction      : 150–200 words. Hook the reader with a relatable scenario or a striking fact \
about female entrepreneurship in India. Establish empathy before authority.
   c. Body sections     : Use frequent subheadings (Title Case) for scannability. \
Minimum 6 substantive sections covering:
      - The current landscape for female entrepreneurs in India (data-backed)
      - Key government schemes tailored for women-led businesses (e.g., Mudra Yojana, Stand-Up India, \
Mahila Udyam Nidhi, TREAD scheme, WE Hub, etc.)
      - Practical tips for accessing credit and overcoming common barriers
      - How expansion financing can unlock the next stage of growth
      - A section that naturally contextualises Credit Saison India's role as an enablement partner
   d. Bullet points and numbered lists: Use liberally for schemes, tips, eligibility criteria, \
and step-by-step processes.
   e. Key Takeaways     : A boxed or clearly separated summary of 5–7 bullet points at the end of the body.


3. INTERNAL LINKS:
   The following links must be embedded within the article body. For each link:
   - Use the specified keyword (or a close natural variant) as the hyperlink anchor text.
   - Prioritise placing the FIRST instance of each link as early as possible — ideally within
     the introduction or the first two body sections. Subsequent instances may be distributed
     across later sections.
   - Embed it exactly the stated number of times across different sections — never in the same paragraph twice.
   - Only place links where they genuinely serve the reader. Do not force or cluster them.
   - Format each as a standard markdown hyperlink: [anchor text](url)

{links_formatted}


4. CALL TO ACTION (final section):
   Tone: Supportive, partnership-first, non-aggressive.
   Goal: Invite the reader to explore expansion financing options with Credit Saison India.
   Format: 2–3 short paragraphs followed by a single, clear CTA button label (e.g., "Explore Your Growth Options").


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SEO & KEYWORD GUIDANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Primary keyword   : financial schemes for women entrepreneurs India
Secondary keywords: women business loan India, MSME loan for women, female entrepreneur funding, \
Mudra loan for women, small business loan Tier 2 cities, business expansion loan India
Integration rule  : Use keywords naturally in headings, the first 100 words, and throughout the body. \
Never stuff or repeat unnaturally.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUALITY CHECKLIST (verify before outputting)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Word count meets or exceeds {word_count} words
☐ Tone is warm and professional throughout — re-read and adjust any section that feels cold or salesy
☐ "Credit Saison India" is never abbreviated
☐ All headings are Title Case; body text is Sentence case
☐ Currency figures use Indian formatting (₹X,XX,XXX)
☐ EMI, KYC, NBFC explained on first use
☐ Each internal link appears exactly the specified number of times with natural anchor text
☐ The first instance of every internal link appears in the introduction or the first two body sections
☐ No two instances of the same link appear in the same paragraph
☐ SEO meta block is complete and within character limits
☐ CTA is encouraging, not pressuring
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
        temperature=0.7,
        max_tokens=6000,
    )

    return response.choices[0].message.content.strip()