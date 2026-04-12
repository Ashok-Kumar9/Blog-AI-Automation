import base64
from app.core.openai_utils import client

BRAND_VISUAL_STYLE = """\
Credit Saison India brand visual style — STRICT PHOTOGRAPHIC REALISM:
- Shot on a professional camera, NOT illustrated, NOT isometric, NOT 3D-rendered, NOT cartoon.
- Colour palette: clean and natural. Slight cool-white or soft daylight tones. \
  Accent touches of deep navy (#004098) or cyan (#19afe1) appear only in clothing, \
  signage, or environmental details — never as artificial overlays.
- Photography style: editorial documentary — like a high-quality stock photo from Getty or Unsplash, \
  but more candid and less posed. Shallow depth of field. Soft bokeh backgrounds.
- Indian context: real Indian faces, hands, workspaces, homes, and streets. \
  Tier-1 to Tier-3 city settings. Business-casual or semi-formal Indian attire.
- Lighting: soft natural window light or warm interior ambient light. \
  No studio flash, no harsh shadows, no artificial glow effects.
- Composition: rule of thirds, slightly off-centre subject. \
  No floating UI elements, no glowing icons, no digital overlays inside the scene.
- Mood: trustworthy, grounded, human — a moment you could actually photograph in real life.\
"""


def build_image_prompt(blog_title: str) -> str:
    """
    Builds a brand-aligned, photorealistic image generation prompt
    for a Credit Saison India blog hero image.

    Args:
        blog_title: The final blog post title. The model infers the
                    scene, subject, and audience entirely from this.

    Returns:
        A detailed prompt string ready for the image generation API.
    """
    return f"""\
Create a photorealistic hero photograph for a Credit Saison India financial blog post \
titled: "{blog_title}".

The image must look like it was taken by a professional photographer — \
NOT illustrated, NOT AI-generated looking, NOT isometric, NOT cartoon or 3D render.

Scene direction:
- Read the blog title carefully and depict a real, believable human moment \
  that is directly and specifically related to its subject matter.
- Show actual people (Indian appearance, authentic expressions) in a recognisable \
  real-world setting — a bank branch, a home office, a notary desk, a small business \
  counter, or a similar environment relevant to the title.
- Focus on hands, documents, faces, or everyday objects that are physically \
  connected to the topic. Examples: a person reviewing paperwork at a desk, \
  a handshake over documents, a close-up of hands signing a form, or someone \
  thoughtfully discussing papers with a professional across a table.
- Avoid symbolic metaphors like floating padlocks, disconnected 3D buildings, \
  or glowing shield icons. Every element in the frame must be a real physical \
  object a person could touch.

Technical photography style:
- Captured on a full-frame DSLR or mirrorless camera (Canon R5 or Sony A7 equivalent).
- Lens: 35mm or 50mm prime, aperture f/1.8–f/2.8 for shallow depth of field.
- Soft, natural window light or warm indoor ambient — no flash, no artificial glow.
- Slight film grain to reinforce authenticity.
- Colour grade: neutral to slightly warm. Clean whites, no oversaturation.
- Composition: rule of thirds, subject slightly off-centre, \
  generous negative space on one side for text overlay.
- No visible text, logos, or watermarks anywhere in the image.

{BRAND_VISUAL_STYLE}

The image must NOT contain:
- Floating or glowing UI icons (padlocks, shields, coins, arrows).
- Isometric or 3D-rendered buildings, objects, or scenes.
- Illustrated or cartoon-style art.
- Abstract digital effects or light-beam overlays.
- Composite scenes where one half is illustration and the other is photo.
- Any visible text, logos, or watermarks.
"""


def generate_blog_image(blog_title: str) -> bytes:
    """
    Generates a brand-aligned, photorealistic hero image for a
    Credit Saison India blog post.

    Args:
        blog_title: The blog post title. All visual context is
                    inferred from this alone.

    Returns:
        Raw PNG image bytes at 1536 x 1024 px (closest API size
        to the target 1500 x 1000 px, landscape orientation).

    Raises:
        ValueError: If the API returns no image data.
        openai.OpenAIError: On API-level failures.
    """
    prompt = build_image_prompt(blog_title)

    response = client.images.generate(
        model="gpt-image-1-mini",
        prompt=prompt,
        size="1536x1024",   # closest supported size to target 1500×1000
        quality="medium",
        output_format="png",
        n=1,
    )

    b64_data = response.data[0].b64_json
    if not b64_data:
        raise ValueError("Image generation returned no data.")

    return base64.b64decode(b64_data)
