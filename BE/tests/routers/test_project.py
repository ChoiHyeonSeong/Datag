import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
import asyncio
import json
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
async def test_create_project(async_client, auth_headers):
    data = {
        "project_name": "New Project",
        "project_model_task": "cls",
        "project_model_name": "efficientnet_v2_s",
        "description": "This is a description of the new project.",
        "accesscontrol": {
            "view_users": ["user1", "user2", "user3"],
            "edit_users": ["user6", "user7", "user10"],
            "view_departments": ["department1", "department2"],
            "edit_departments": ["department3", "department4"]
        },
        "is_private": 0
    }
    
    response = await async_client.post(
        "be/api/project/create",
        json=data,
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert "data" in response.json()
    return response.json()["data"]

@pytest.mark.asyncio
async def test_get_project_list(async_client, auth_headers):
    params = {
        "page": 1,
        "limit": 10
    }

    response = await async_client.get(
        "be/api/project/list",
        params=params,
        headers=auth_headers
    )

    print(f"Response Content: {response.content}")

    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert isinstance(response.json()["data"]['data'], list)

@pytest.mark.asyncio
async def test_delete_project(async_client, auth_headers):
    project_id = await test_create_project(async_client, auth_headers)
    
    response = await async_client.delete(f"be/api/project/delete/{project_id}", headers=auth_headers)
    
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_department_list(async_client):
    response = await async_client.get("be/api/department/list")
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert isinstance(response.json()["data"], list)

@pytest.mark.asyncio
async def test_search_user_name(async_client, auth_headers):
    params = {
        "page": 1,
        "limit": 10
    }
    response = await async_client.get("be/api/user/search", params=params, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert "limit" in response.json()["data"]
    assert "page" in response.json()["data"]
    assert "total_count" in response.json()["data"]

@pytest.mark.asyncio
async def test_filter_image_add(async_client, auth_headers):
    # 먼저 프로젝트를 생성
    project_id = await test_create_project(async_client, auth_headers)
    
    add_filtering_image_request = {
        "project_id": project_id,
        "conditions": [
            {
                "and_condition": ["cat", "Seoul"],
                "or_condition": ["2024_11"],
                "not_condition": ["Zone A"]
            }
        ]
    }

    response = await async_client.post(
        f"be/api/project/filterImage/{project_id}/list",
        json=add_filtering_image_request,
        headers=auth_headers
    )
    
    print(f"Response content: {response.content}")

    assert response.status_code == 200

    assert isinstance(response.json()["data"]["image_list"], list)