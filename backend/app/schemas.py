from datetime import datetime
from pydantic import BaseModel, HttpUrl


class FeedCreate(BaseModel):
    url: HttpUrl


class FeedResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    url: str
    title: str
    created_at: datetime


class ArticleResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    title: str | None = None
    url: str
    summary: str | None = None
    published_at: datetime | None = None
