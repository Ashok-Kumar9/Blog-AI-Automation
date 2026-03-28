from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.models.schemas import TopicRequest, TopicResponse, BlogRequest, BlogResponse
from app.services.title_generator import generate_trending_topics
from app.services.blog_generator import generate_blog
import os

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="Professional API for Blog Topic and Content Generation."
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Static Files ---

# Create frontend directory if it doesn't exist
os.makedirs("frontend", exist_ok=True)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")


# --- API Endpoints ---

@app.get("/api/defaults")
async def get_defaults():
    """Returns default settings for the frontend to pre-fill forms."""
    return {
        "category": settings.DEFAULT_BLOG_CATEGORY,
        "competitors": settings.DEFAULT_COMPETITORS,
        "audience": settings.DEFAULT_TARGET_AUDIENCE,
        "word_count": settings.DEFAULT_WORD_COUNT_GOAL,
        "goal": settings.DEFAULT_SPECIFIC_GOAL,
        "internal_links": settings.DEFAULT_INTERNAL_LINKS
    }

@app.get("/health")
async def health_check():
    return {"status": "online health", "message": f"{settings.APP_TITLE} is running"}

@app.post("/api/generate-topics", response_model=TopicResponse)

async def api_generate_topics(request: TopicRequest):
    try:
        topics = generate_trending_topics(request.category, request.competitors)
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
