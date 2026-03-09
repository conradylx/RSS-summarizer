from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Feed
from app.schemas import FeedCreate, FeedResponse

router = APIRouter(prefix="/feeds", tags=["feeds"])


@router.get("/", response_model=list[FeedResponse])
async def list_feeds(db: Annotated[AsyncSession, Depends(get_db)]):
    results = await db.execute(select(Feed))
    return results.scalars().all()


@router.post("/", response_model=FeedResponse)
async def create_feed(
    data: FeedCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    existing = await db.execute(select(Feed).where(Feed.url == str(data.url)))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Feed already exists")

    feed = Feed(url=str(data.url))
    db.add(feed)
    await db.commit()
    await db.refresh(feed)
    return feed


@router.delete("/{feed_id}", status_code=204)
async def delete_feed(
    feed_id: int, db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(Feed).where(Feed.id == feed_id))
    feed = result.scalar_one_or_none()
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")

    await db.delete(feed)
    await db.commit()
