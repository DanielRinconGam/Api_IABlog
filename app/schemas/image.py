from pydantic import BaseModel, HttpUrl
from typing import Optional


class ImageCreate(BaseModel):
    url: HttpUrl
    description: Optional[str] = None


class ImageOut(ImageCreate):
    id: int

    class Config:
        from_attributes = True
