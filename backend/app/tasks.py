from datetime import datetime
import feedparser
from sqlalchemy import select
from app.services.summarizer import summarize
from app.celery_utils import run_async_in_celery
from app.database import AsyncSessionLocal
from app.worker import celery_app
from app.models import Feed, Article


async def _fetch_feed(feed_id: int) -> None:
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Feed).where(Feed.id == feed_id))
        feed = result.scalar_one_or_none()
        if not feed:
            return
        parsed = feedparser.parse(feed.url)
        if not feed.title and parsed.feed.get("title"):
            feed.title = parsed.feed.title
        for entry in parsed.entries:
            link = entry.get("link")
            guid = entry.get("id") or entry.get("guid")
            url = link or guid
            if not url:
                continue

            existing = await db.execute(
                select(Article).where(Article.url == url)
            )
            if existing.scalar_one_or_none():
                continue

            published_raw = entry.get("published_parsed")
            published_at = (
                datetime(*published_raw[:6])
                if published_raw
                else None  # type: ignore
            )
            article = Article(
                feed_id=feed_id,
                title=entry.get("title", "No title"),
                url=url,
                content=entry.get("summary"),
                published_at=published_at,
            )
            article.summary = summarize(article.content)
            db.add(article)
        await db.commit()


async def _fetch_all_feeds() -> None:
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Feed))
        feeds = result.scalars().all()
        for feed in feeds:
            fetch_feed.delay(feed.id)  # type: ignore[attr-defined]


@celery_app.task
def fetch_feed(feed_id: int, max_retries=0) -> None:
    run_async_in_celery(_fetch_feed(feed_id))


@celery_app.task
def fetch_all_feeds() -> None:
    run_async_in_celery(_fetch_all_feeds())
