import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.mark.anyio
async def test_get_articles_empty(client):
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute.return_value = mock_result

    async def fake_db():
        yield mock_session

    from app.main import app
    from app.database import get_db

    app.dependency_overrides[get_db] = fake_db

    response = await client.get("/articles/")
    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_get_article_not_found(client):
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    async def fake_db():
        yield mock_session

    from app.main import app
    from app.database import get_db

    app.dependency_overrides[get_db] = fake_db

    response = await client.get("/articles/999")
    assert response.status_code == 404

    app.dependency_overrides.clear()
