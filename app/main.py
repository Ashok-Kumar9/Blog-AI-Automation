from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.models.schemas import TopicRequest, TopicResponse, BlogRequest, BlogResponse, ImageRequest, ImageResponse
from app.services.title_generator import generate_trending_topics
from app.services.blog_generator import generate_blog, InternalLink
from app.services.image_generator import generate_blog_image
import base64

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="Professional API for Blog Topic and Content Generation."
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # During development, allowing all is fine; specify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/")
@app.get("/health")
async def health_check():
    """Diagnostic endpoint to verify the backend is online."""
    return {
        "status": "online",
        "message": f"{settings.APP_TITLE} is active",
        "version": settings.APP_VERSION
    }



@app.post("/api/generate-topics", response_model=TopicResponse)
async def api_generate_topics(request: TopicRequest):
    try:
        topics = generate_trending_topics(request.category)
        return TopicResponse(category=request.category, topics=topics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-blog", response_model=BlogResponse)
async def api_generate_blog(request: BlogRequest):
    try:
        # Map Pydantic models to InternalLink dataclasses
        internal_links = [
            InternalLink(
                product_keyword=link.product_keyword,
                url=link.url,
                integration_count=link.integration_count
            )
            for link in request.internal_links
        ]

        content = generate_blog(
            topic=request.topic,
            audience=request.target_audience,
            word_count=request.word_count_goal,
            specific_goal=request.specific_goal,
            internal_links=internal_links
        )
        return BlogResponse(topic=request.topic, content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-image", response_model=ImageResponse)
async def api_generate_image(request: ImageRequest):
    try:
        image_bytes = generate_blog_image(
            blog_title=request.blog_title
        )
        base64_str = base64.b64encode(image_bytes).decode("utf-8")
        return ImageResponse(image_base64=base64_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

