from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Article
from ..schemas import ArticleResponse
from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=list[ArticleResponse])
async def get_articles(
    db: Annotated[AsyncSession, Depends(get_db)], feed_id: int | None = None
):
    query = select(Article).order_by(Article.published_at.desc())
    if feed_id:
        query = query.where(Article.feed_id == feed_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
