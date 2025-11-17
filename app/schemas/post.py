from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.image import ImageCreate, ImageOut

class PromptRequest(BaseModel):
    prompt: str

class PostCreate(BaseModel):
    title: str
    body: str
    seo_description: Optional[str] = None
    images: List[ImageCreate] = []

class PostOut(BaseModel):
    id: int
    title: str
    body: str
    seo_description: Optional[str]
    author_id: int
    created_at: datetime
    images: List[ImageOut]

    class Config:
        from_attributes = True
