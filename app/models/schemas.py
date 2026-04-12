from typing import List
from pydantic import BaseModel

class TopicRequest(BaseModel):
    category: str

class InternalLinkSchema(BaseModel):
    product_keyword: str
    url: str
    integration_count: int

class BlogRequest(BaseModel):
    topic: str
    target_audience: str
    word_count_goal: int
    specific_goal: str
    internal_links: List[InternalLinkSchema]

class TopicResponse(BaseModel):
    category: str
    topics: List[str]

class BlogResponse(BaseModel):
    topic: str
    content: str

class ImageRequest(BaseModel):
    blog_title: str

class ImageResponse(BaseModel):
    image_base64: str
