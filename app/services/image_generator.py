from app.core.model_layer import llm_provider

# -------------------------------
# MODE SWITCH
# -------------------------------
PHOTOREALISTIC = "photo"
CONCEPTUAL = "concept"


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
- NEVER use colors as overlays, gradients, glowing effects, or UI elements (in photo mode)
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
# PROMPT BUILDER
# -------------------------------
def build_image_prompt(blog_title: str, mode: str = PHOTOREALISTIC) -> str:

    if mode == PHOTOREALISTIC:
        return f"""\
Create a photorealistic hero image for:
"{blog_title}"

STRICT RULES:
- Real Indian people only
- Natural expressions, candid moment
- Real environments (home, office, bank, shop)
- DSLR-style photography

Scene:
- Show a real-life financial interaction
- Focus on hands, documents, discussion

Style:
- Shot on 35mm/50mm lens
- Shallow depth of field
- Natural lighting only

Avoid:
- No icons, no UI overlays
- No illustrations
- No 3D objects
- No text

{BRAND_VISUAL_STYLE}
"""

    # -------------------------------
    # NEW: CONCEPTUAL EXPLAINER MODE
    # -------------------------------
    elif mode == CONCEPTUAL:
        return f"""\
Create a clean, modern, conceptual financial explainer image for:
"{blog_title}"

STYLE:
- Semi-realistic illustration (NOT cartoon, NOT fully photorealistic)
- Clean, minimal, professional fintech visual
- Soft gradient background (white to light blue)

LAYOUT:
- Split composition (left and right sections)

LEFT SIDE:
- A simplified but realistic 3D-style object representing the topic
  (e.g., house, document, building, money, property)
- Slight isometric or soft 3D perspective allowed

RIGHT SIDE:
- Human interaction or object interaction
- Example: hands exchanging documents, signing papers, reviewing file

CENTER CONNECTION:
- Subtle connector element (line, lock icon, or shield)
- MUST be minimal and not glowing or flashy

STYLE RULES:
- No clutter
- No heavy shadows
- No dramatic lighting
- Soft depth and subtle shadows only

COLOR:
- White background dominant
- Use brand blue (#004098) and cyan (#19afe1) minimally
- No harsh contrast

STRICTLY AVOID:
- Cartoon style
- Overly realistic photography
- Heavy UI dashboards
- Text or labels
- Complex scenes

MOOD:
- Informative
- Clean
- Easy to understand visually

{BRAND_VISUAL_STYLE}
"""

    else:
        raise ValueError("Invalid mode. Use 'photo' or 'concept'.")


# -------------------------------
# GENERATOR
# -------------------------------
def generate_blog_image(blog_title: str, mode: str = PHOTOREALISTIC) -> bytes:
    prompt = build_image_prompt(blog_title, mode)
    return llm_provider.gemini.generate_image(prompt)