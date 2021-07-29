import pytest
import json
from httpx import AsyncClient

from app.main import app

@pytest.mark.asyncio
async def test_ping():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/ping")
    assert response.status_code == 200
    assert json.dumps(eval(response.text)) == json.dumps({'result': 'pong'})