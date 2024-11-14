from httpx import AsyncClient
import asyncio
import pytest
import json
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.main import app
from app.configs.mariadb import get_database_mariadb
from app.configs.mongodb import client as mongo_client

from unittest.mock import Mock, patch

client = TestClient(app)

def get_auth_token():
    login_data = {
        "email": "test1@tmail.ws",  
        "password": "1234"
    }
    
    # 로그인 요청
    response = client.post("be/api/auth/login", json=login_data)
    assert response.status_code == 200 
    
    # 토큰 추출
    token = response.json()["data"].get("access_token")
    assert token is not None, "토큰이 반환되지 않았습니다."
    
    return token

@pytest.fixture
def auth_headers():
    token = get_auth_token()
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="session")
async def mongodb():
    result = await mongo_client.admin.command("ping")
    assert result["ok"] != 0.0  # Check that the connection is okay.
    return mongo_client

# 1. 프로젝트 생성 테스트
@pytest.mark.asyncio
async def test_create_project(auth_headers, mongodb):
    mongodb_instance = await mongodb

    data = {
            "user_id": 1,
            "project_name": "New Project",
            "model_name": "vgg19_bn",
            "description": "This is a description of the new project.",
            "accesscontrol": {
                "view_users": ["user1", "user2", "user3"],
                "edit_users": ["user6", "user7", "user10"],
                "view_departments": ["department1", "department2"],
                "edit_departments": ["department3", "department4"]
            },
            "is_private": 0
        }
    
    session = mongodb_instance.start_session()
    session.start_transaction()
    
    response = client.post(
        "be/api/project/create",
        json=data,
        headers=auth_headers
    )

    session.abort_transaction()

    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert "data" in response.json()

# 2. 프로젝트 리스트 조회 테스트
@pytest.mark.asyncio
async def test_get_project_list(auth_headers):
    params={
        "page" : 1,
        "limit" : 10
        }
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        response = await client.get(
            "be/api/project/list",
            params=params,
            headers=auth_headers
        )

    print(response.json())
    
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert isinstance(response.json()["data"]['data'], list)

# 3. 프로젝트 삭제 테스트
@pytest.mark.asyncio
async def test_delete_project():
    session = mongo_client.start_session()
    session.start_transaction()

    # 삭제할 프로젝트 ID가 1이라고 가정
    response = client.delete("be/api/project/1",headers=auth_headers)

    session.abort_transaction()

    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert response.json()["data"]["message"] == "Project deleted successfully"

# 4. 부서 리스트 조회 테스트
@pytest.mark.asyncio
async def test_get_department_list():
    response = client.get("be/api/department/list")
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert isinstance(response.json()["data"], list)

# 5. 사용자 이름 검색 테스트
@pytest.mark.asyncio
async def test_search_user_name(auth_headers):
    params = {
        "page" :1,
        "limit" : 10
    }
    response = client.get("be/api/user/search", params=params, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert isinstance(response.json()["data"], list)

# 6. 프로젝트에 필터링된 이미지 저장
def test_filter_image_add(auth_headers, mock_upload_service, mock_db):
    add_filtering_image_request = {
    "project_id": "6732f477fcec9d2c66a7507c",
    "conditions":
        [
            {
            "and_condition": ["cat", "Seoul"],
            "or_condition": ["2024_11"],
            "not_condition": ["Zone A"]
            }
        ]
    }
    
    session = mongo_client.start_session()
    session.start_transaction()

    response = client.post(
        "be/api/project/filterImage/{project_id}/list",
        data={"add_filtering_image_request": json.dumps(add_filtering_image_request)},
        headers=auth_headers
    )

    session.abort_transaction()

    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": "이미지 업로드에 성공하였습니다."
    }

    mock_upload_service.return_value.upload_image.assert_called_once()
    assert isinstance(response.json()["data"]['data'], list)
