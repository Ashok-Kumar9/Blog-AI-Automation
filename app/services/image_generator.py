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
    return llm_provider.openai.generate(
        user_prompt=f"""\
Search online and identify the key visual elements for this blog topic:
"{blog_title}"

Describe a realistic scene that would visually represent this topic in an Indian context. Cover:
- The setting (physical location or environment most associated with this topic)
- The people (who is typically involved — their profile, age group, gender, attire)
- The objects or props that would naturally appear in this scenario
- Any relevant cultural, seasonal, or situational context specific to India

Return 2-3 concise, visual-focused sentences only. Do not include brand names, text, or UI elements."""
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
Scene:
- Show one or two real people fully visible in a natural, everyday Indian setting relevant to the topic
- People should be the focal point — show their full body or at least from the waist up, with faces clearly visible and engaged in a natural activity
- Include contextually relevant objects or documents in the scene
- The environment and people's attire should feel authentically Indian

People:
- Faces must be fully visible, expressive, and naturally lit
- Avoid cropped heads, obscured faces, or faceless figures
- Body language should convey the emotion or action relevant to the topic (confidence, concern, discussion, relief, etc.)

Composition:
- Balanced framing with people as the subject
- Background should be soft but contextually relevant
- Bright, airy, and uncluttered scene

Avoid:
- No icons, no UI overlays
- No illustrations or 3D renders
- No text or labels in the image
- No disembodied hands or partial figures as the main subject

{BRAND_VISUAL_STYLE}
"""


# -------------------------------
# GENERATOR
# -------------------------------
def generate_blog_image(blog_title: str) -> bytes:
    research_context = _research_topic(blog_title)
    prompt = build_image_prompt(blog_title, research_context)
    return llm_provider.gemini.generate_image(prompt)
