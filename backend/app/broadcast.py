import json
from typing import Any, AsyncGenerator
import redis.asyncio as aioredis
from app.config import settings

CHANNEL = "new_articles"


async def publish_article(article_data: dict[str, Any]) -> None:
    if not article_data:
        return
    r = aioredis.from_url(settings.redis_url)
    try:
        await r.publish(CHANNEL, json.dumps(article_data))
    finally:
        await r.aclose()


async def subscribe_articles() -> AsyncGenerator[dict[str, Any], None]:
    r = aioredis.from_url(settings.redis_url)
    pubsub = r.pubsub()
    await pubsub.subscribe(CHANNEL)
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                yield json.loads(message["data"])
    finally:
        await pubsub.unsubscribe(CHANNEL)
        await r.aclose()
