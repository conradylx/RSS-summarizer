import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.anyio
@patch("app.routers.feeds.fetch_feed")
@patch("app.routers.feeds.get_db")
async def test_list_feeds_empty(mock_get_db, mock_fetch_feed, client):
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute.return_value = mock_result

    async def fake_db():
        yield mock_session

    from app.main import app
    from app.database import get_db

    app.dependency_overrides[get_db] = fake_db

    response = await client.get("/feeds/")
    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_create_feed_returns_409_for_duplicate(client):
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = MagicMock()
    mock_session.execute.return_value = mock_result

    async def fake_db():
        yield mock_session

    from app.main import app
    from app.database import get_db

    app.dependency_overrides[get_db] = fake_db

    response = await client.post(
        "/feeds/", json={"url": "https://example.com/rss"}
    )
    assert response.status_code == 409

    app.dependency_overrides.clear()
