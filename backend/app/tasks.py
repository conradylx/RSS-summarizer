from datetime import datetime
import feedparser
import logging
from sqlalchemy import select
from app.services.summarizer import summarize
from app.celery_utils import run_async_in_celery
from app.database import AsyncSessionLocal
from app.worker import celery_app
from app.models import Feed, Article
from app.broadcast import publish_article

logger = logging.getLogger(__name__)


async def _fetch_feed(feed_id: int) -> None:
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Feed).where(Feed.id == feed_id))
        feed = result.scalar_one_or_none()
        if not feed:
            logger.warning(f"[{feed_id}] Feed not found")
            return

        parsed = feedparser.parse(feed.url)
        logger.info(f"[{feed_id}] Parsed {len(parsed.entries)} entries from {feed.url}")

        if not feed.title and parsed.feed.get("title"):
            feed.title = parsed.feed.title
            await db.commit()

        existing_urls = set((await db.execute(select(Article.url))).scalars().all())

    new_count = 0
    for entry in parsed.entries:
        link = entry.get("link")
        guid = entry.get("id") or entry.get("guid")
        url = link or guid
        if not url or url in existing_urls:
            continue

        published_raw = entry.get("published_parsed")
        published_at = datetime(*published_raw[:6]) if published_raw else None
        title = entry.get("title", "No title")

        logger.info(f"[{feed_id}] Summarizing: {title}")
        await publish_article(
            {
                "type": "status",
                "feed_id": feed_id,
                "status": "summarizing",
                "title": title,
            }
        )

        summary = summarize(entry.get("summary"))

        # Commit po każdym artykule osobno
        async with AsyncSessionLocal() as db:
            article = Article(
                feed_id=feed_id,
                title=title,
                url=url,
                content=entry.get("summary"),
                summary=summary,
                published_at=published_at,
            )
            db.add(article)
            await db.commit()
            await db.refresh(article)
            logger.info(f"[{feed_id}] Saved: {title}")
            await publish_article(
                {
                    "type": "article",
                    "id": article.id,
                    "title": article.title,
                    "url": article.url,
                    "summary": article.summary,
                    "published_at": (
                        str(article.published_at) if article.published_at else None
                    ),
                }
            )
            new_count += 1

    if new_count == 0:
        logger.info(f"[{feed_id}] No new articles")

    await publish_article(
        {
            "type": "status",
            "feed_id": feed_id,
            "status": "done",
        }
    )


async def _fetch_all_feeds() -> None:
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Feed))
        feeds = result.scalars().all()
        for feed in feeds:
            fetch_feed.delay(feed.id)  # type: ignore[attr-defined]


@celery_app.task
def fetch_feed(feed_id: int) -> None:
    run_async_in_celery(_fetch_feed(feed_id))


@celery_app.task
def fetch_all_feeds() -> None:
    run_async_in_celery(_fetch_all_feeds())
