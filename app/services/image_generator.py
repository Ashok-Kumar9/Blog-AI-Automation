from app.core.model_layer import llm_provider

BRAND_VISUAL_STYLE = """\
Credit Saison India brand visual system — STRICT ADHERENCE REQUIRED:

COLOR SYSTEM (MANDATORY COMPOSITION BALANCE):
- White (#ffffff) ~40% → Primary background base
- Saison Blue (#004098) ~30% → Primary brand color (clothing, key objects, accents)
- Accent Blue (#19afe1) ~10% → Secondary highlights (subtle elements only)
- Grey (#f2f2f2) ~10% → Background surfaces, walls, tables
- Accent Green (#009944) ~5% → Minimal highlights (plants, files, indicators)
- Black (#000000) ~5% → Textural depth (hair, shadows, contrast)

APPLICATION RULES:
- Colors MUST appear as part of real-world objects only
  (clothing, furniture, walls, documents, environment)
- NEVER use colors as overlays, gradients, glowing effects, or UI elements
- Avoid oversaturation — tones must remain natural and balanced
- White/light backgrounds should dominate the scene visually

COMPOSITION BALANCE:
- Scene must feel bright, clean, and uncluttered
- Blue tones should guide visual hierarchy, not overpower
- No single color should dominate excessively beyond its proportion

STYLE:
- Clean, modern, minimal
- Trustworthy financial brand tone
"""


# -------------------------------
# WEB RESEARCH
# -------------------------------
def _research_topic(blog_title: str) -> str:
    return llm_provider.gemini.generate(
        user_prompt=f"""\
Search online and find key visual elements for this Indian personal finance blog topic:
"{blog_title}"

Focus specifically on the Indian context:
- What real-world Indian setting best represents this topic?
  (e.g. a PSU bank branch, an NBFCs office, a urban apartment, a kirana shop, a government office)
- Who are the typical people involved?
  (e.g. salaried professional in Mumbai, farmer in rural Maharashtra, small business owner, homemaker)
- What Indian-specific objects, documents, or props are present?
  (e.g. Aadhaar card, PAN card, passbook, salary slip, GST invoice, UPI QR code, gold jewellery)
- Any relevant Indian cultural or seasonal context?
  (e.g. festival season purchase, tax-filing deadline, agricultural cycle, wedding expenses)

Return 2-3 concise, visual-focused sentences only."""
    )


# -------------------------------
# PROMPT BUILDER
# -------------------------------
def build_image_prompt(blog_title: str, research_context: str = "") -> str:
    context_section = (
        f"\nTopic Context (from web research):\n{research_context}\n"
        if research_context
        else ""
    )

    return f"""\
Create a photorealistic hero image for this Indian personal finance blog:
"{blog_title}"
{context_section}
PEOPLE:
- Real Indian people only — South Asian skin tones, Indian facial features
- Authentic ethnic diversity (North, South, East, West Indian appearances)
- Clothing: contemporary Indian casuals or formals — kurta, saree, salwar, office wear
- Natural expressions — no posed smiles, candid moments only
- Age range appropriate to the topic (young professional, middle-aged couple, senior citizen)

SETTING:
- Authentic Indian environments — a bank branch with Hindi signage, a modest urban flat,
  a semi-urban market, a government office, a jewellery shop, an NBFC counter
- Indian props where relevant: Aadhaar / PAN card, passbook, salary slip, GST bill,
  UPI QR code, gold jewellery, fixed deposit receipt, insurance policy document
- Natural Indian light — warm afternoon sunlight through a window, tube-light office,
  open-air market shade

SCENE:
- Show the real-life financial interaction described in the topic context above
- Focus on the human moment: hands exchanging documents, signing papers,
  reviewing a phone screen, counting currency, discussing at a counter

PHOTOGRAPHY STYLE:
- Shot on 35mm or 50mm prime lens
- Shallow depth of field, subject sharp, background softly blurred
- Natural or available light — no studio flash
- Warm, slightly desaturated tones — feels like real India, not a stock photo

STRICTLY AVOID:
- Western or generic Asian appearances
- Clean, sterile Western office environments
- Icons, UI overlays, illustrations, 3D objects, or text
- Overly bright or artificially lit studio setups
- Tourist-India clichés (Taj Mahal, saffron, elephants)

{BRAND_VISUAL_STYLE}
"""


# -------------------------------
# GENERATOR
# -------------------------------
def generate_blog_image(blog_title: str) -> bytes:
    research_context = _research_topic(blog_title)
    prompt = build_image_prompt(blog_title, research_context)
    return llm_provider.gemini.generate_image(prompt)
