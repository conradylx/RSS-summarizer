from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class FeedCreate(BaseModel):
    url: HttpUrl
    title: Optional[str] = None


class FeedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    title: str = Field(default="Untitled")
    created_at: datetime


class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str | None = None
    url: str
    summary: str | None = None
    published_at: datetime | None = None
