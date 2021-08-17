import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../app')

import pytest
import json
from httpx import AsyncClient

from app.main import app
import app.schemas.base_response as base_response_schema


@pytest.mark.asyncio
async def test_ping():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/ping")
    assert response.status_code == 200
    assert json.dumps(response.json()) == base_response_schema.BaseResponse(result=True).json()