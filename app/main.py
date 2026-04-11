from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.models.schemas import TopicRequest, TopicResponse, BlogRequest, BlogResponse
from app.services.title_generator import generate_trending_topics
from app.services.blog_generator import generate_blog

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

@app.get("/api/defaults")
async def get_defaults():
    """Returns default values for the frontend to pre-fill forms."""
    return {
        "category": settings.DEFAULT_BLOG_CATEGORY,
        "competitors": settings.DEFAULT_COMPETITORS,
        "audience": settings.DEFAULT_TARGET_AUDIENCE,
        "word_count": settings.DEFAULT_WORD_COUNT_GOAL,
        "goal": settings.DEFAULT_SPECIFIC_GOAL,
        "internal_links": settings.DEFAULT_INTERNAL_LINKS
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
        content = generate_blog(
            topic=request.topic,
            audience=request.target_audience,
            word_count=request.word_count_goal,
            specific_goal=request.specific_goal,
            internal_links=request.internal_links
        )
        return BlogResponse(topic=request.topic, content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

