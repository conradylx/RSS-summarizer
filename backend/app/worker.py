from celery import Celery
from app.config import settings

celery_app = Celery(
    "RSSsummarizer",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks"],
)

celery_app.conf.update(task_serializer="json", result_serializer="json", timezone="UTC")
celery_app.conf.beat_schedule = {
    "fetch-all-feeds-every-10-minutes": {
        "task": "app.tasks.fetch_all_feeds",
        "schedule": 60.0 * 10,
    },
}
