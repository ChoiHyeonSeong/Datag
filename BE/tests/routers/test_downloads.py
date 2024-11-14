import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from app.main import app

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

@pytest.mark.asyncio
async def test_download_success(async_client, auth_headers):
    request_data = {
        "image_list": ["67357126059951d450e45838"]
    }
    response = await async_client.post("be/api/image/download", json=request_data, headers=auth_headers)
    
    print(f"Response content: {response.content}")
    
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_download_unauthorized(async_client):
    request_data = {
        "image_list": ["67357126059951d450e45838"]
    }
    response = await async_client.post("be/api/image/download", json=request_data)
    
    assert response.status_code == 403  # 인증 실패

@pytest.mark.asyncio
async def test_download_invalid_data(async_client, auth_headers):
    invalid_data = {"invalid_key": "invalid_value"}
    response = await async_client.post("be/api/image/download", json=invalid_data, headers=auth_headers)
    
    assert response.status_code == 422  # 유효성 검사 실패

@pytest.mark.asyncio
async def test_download_empty_list(async_client, auth_headers):
    request_data = {
        "image_list": []
    }
    response = await async_client.post("be/api/image/download", json=request_data, headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "이미지가 존재하지 않습니다."
