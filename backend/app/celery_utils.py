import asyncio
from collections.abc import Coroutine
from typing import Any


def run_async_in_celery(coro: Coroutine[Any, Any, None]) -> None:
    asyncio.run(coro)
