from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
import pytest

import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from app.main import app

@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# @pytest.fixture(scope="class")
# def db_client(event_loop):
#     client = MongoDBClient()
#     motor_client = AsyncIOMotorClient(f"mongodb://{SETTINGS.mongodb_host}:{SETTINGS.mongodb_port}", io_loop=event_loop)
#     client._client = motor_client
#     client._db_name = "testDB"
#     client._db = motor_client["testDB"]
#     yield client
#     event_loop.run_until_complete(client.drop_database())
#     client.close()

@pytest.fixture(scope="module")
async def async_client():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
            yield client

@pytest.fixture(scope="module")
async def auth_headers(async_client):
    login_data = {
        "email": "test1@tmail.ws",  
        "password": "1234"
    }
    
    response = await async_client.post("be/api/auth/login", json=login_data)
    assert response.status_code == 200 
    
    token = response.json()["data"].get("access_token")
    assert token is not None, "토큰이 반환되지 않았습니다."
    
    return {"Authorization": f"Bearer {token}"}