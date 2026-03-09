import asyncio
from typing import Awaitable


def run_async_in_celery(coro: Awaitable) -> None:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    future = asyncio.ensure_future(coro)
    loop.run_until_complete(future)
