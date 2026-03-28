from typing import List, Optional
from pydantic import BaseModel, Field
from app.core.config import settings

class TopicRequest(BaseModel):
    category: str = Field(default=settings.DEFAULT_BLOG_CATEGORY)
    competitors: List[str] = Field(default=settings.DEFAULT_COMPETITORS)

class BlogRequest(BaseModel):
    topic: str
    target_audience: str = Field(default=settings.DEFAULT_TARGET_AUDIENCE)
    word_count_goal: int = Field(default=settings.DEFAULT_WORD_COUNT_GOAL)
    specific_goal: str = Field(default=settings.DEFAULT_SPECIFIC_GOAL)
    internal_links: List[str] = Field(default=settings.DEFAULT_INTERNAL_LINKS)

class TopicResponse(BaseModel):
    category: str
    topics: List[str]

class BlogResponse(BaseModel):
    topic: str
    content: str
