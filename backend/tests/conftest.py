import pytest
from unittest.mock import patch, MagicMock
from httpx import ASGITransport, AsyncClient

fake_settings = MagicMock()
fake_settings.database_url = "sqlite+aiosqlite:///test.db"
fake_settings.redis_url = "redis://localhost:6379"
fake_settings.ollama_url = "http://localhost:11434/v1"

with patch("app.config.settings", fake_settings):
    from app.main import app


@pytest.fixture
def anyio_backend():
    """Use the asyncio backend for anyio tests."""
    return "asyncio"


@pytest.fixture
async def client():
    """Provides an HTTP client for testing the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
