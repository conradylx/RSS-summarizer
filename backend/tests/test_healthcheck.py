import pytest


@pytest.mark.anyio
async def test_healthcheck_returns_200(client):
    response = await client.get("/healthcheck")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
