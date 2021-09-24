# External libraries
from http import HTTPStatus

import pytest
from httpx import AsyncClient

# Internal libraries
from main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"STATUS": "Klinesso Recommender API"}
