# External libraries
from http import HTTPStatus

import pytest
from httpx import AsyncClient

# Internal libraries
from main import app


@pytest.mark.asyncio
async def test_get():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/recommend/The Thrill is Gone")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'Recommendations':
            [
                'Halte durch',
                'Dont Tell Me That Its Over',
                'Purple Haze',
                'Stormy Monday',
                'The Trooper'
            ],
    }
