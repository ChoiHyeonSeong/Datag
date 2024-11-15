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

# 1. 이미지 정보 조회
@pytest.mark.asyncio
async def test_get_image_detail(async_client, auth_headers):
    data = {
            "project_id": "6732f477fcec9d2c66a7507c",
            "image_id": "6732f4f8db3183653e78ac53",
            "conditions": [
                {
                    "and_condition": [],
                    "or_condition": [],
                    "not_condition": []
                }
            ]
        }
    
    response = await async_client.post(
        f"be/api/image/detail/{data['project_id']}/{data['image_id']}",
        json=data,
        headers=auth_headers
    )
    print(response.json())

    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert "data" in response.json()
    return response.json()["data"]

# 2. 이미지 조회
@pytest.mark.asyncio
async def test_search_images(async_client, auth_headers):
    data = {
            "page": 1,
            "limit": 10,
            "conditions": [
                {
                    "and_condition": ["cat", "Seoul"],
                    "or_condition": ["2024_11"],
                    "not_condition": ["Zone A"]
                }
            ]
        }
    
    response = await async_client.post(
        "be/api/image/search",
        json=data,
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert "data" in response.json()
    return response.json()["data"]

# 3. 해당 이미지 부서 권한 추가
@pytest.mark.asyncio
async def test_add_department_permission(async_client, auth_headers):
    data = {
            "image_id": "6732f4f3db3183653e78ac44",
            "department_name_list": ["Research and Development", "Computer"]
        }
    
    response = await async_client.post(
        "be/api/image/permission/addDepartment",
        json=data,
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert "data" in response.json()
    return response.json()["data"]

# 4. 해당 이미지 유저 권한 추가
@pytest.mark.asyncio
async def test_add_user_permission(async_client, auth_headers):
    data = {
            "image_id": "6732f4f3db3183653e78ac44",
            "user_id_list": ["1", "2"]
        }

    response = await async_client.post(
        "be/api/image/permission/addUser",
        json=data,
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert "data" in response.json()
    return response.json()["data"]

# # 5. 해당 이미지 부서 권한 삭제
# @pytest.mark.asyncio
# async def test_remove_department_permission(async_client, auth_headers):
#     data = {
#             "image_id": "6732f4f3db3183653e78ac44",
#             "department_name_list": ["Computer", "Research and Development"]
#         }

#     response = await async_client.post(
#         "be/api/image/permission/removeDepartment",
#         json=data,
#         headers=auth_headers
#     )

#     assert response.status_code == 200
#     assert response.json()["status"] == 200
#     assert "data" in response.json()
#     return response.json()["data"]

# # 6. 해당 이미지 유저 권한 삭제
# @pytest.mark.asyncio
# async def test_remove_user_permission(async_client, auth_headers):

#     data = {
#             "image_id": "6732f4f3db3183653e78ac44",
#             "user_id_list": ["1", "2"]
#         }

#     response = await async_client.post(
#         "be/api/image/permission/removeUser",
#         json=data,
#         headers=auth_headers
#     )

#     assert response.status_code == 200
#     assert response.json()["status"] == 200
#     assert "data" in response.json()
#     return response.json()["data"]

# 7. 해당 이미지에 태그 추가
@pytest.mark.asyncio
async def test_add_image_tag(async_client, auth_headers):
    data = {
            "image_id": "6732f4f3db3183653e78ac44",
            "tag_list": ["dog", "cat"]
        }
    
    response = await async_client.post(
        "be/api/image/tag/add",
        json=data,
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert "data" in response.json()
    return response.json()["data"]

# # 8. 해당 이미지에 태그 삭제
# @pytest.mark.asyncio
# async def test_remove_image_tag(async_client, auth_headers):
#     data = {
#             "image_id": "str",
#             "remove_tag_list": ["dog", "cat"]
#         }

#     response = await async_client.post(
#         "be/api/image/tag/remove",
#         json=data,
#         headers=auth_headers
#     )

#     assert response.status_code == 200
#     assert response.json()["status"] == 200
#     assert "data" in response.json()
#     return response.json()["data"]

# 9. 태그 리스트 불러오기
@pytest.mark.asyncio
async def test_get_tags_and_images(async_client, auth_headers):
    response = await async_client.get(
        "be/api/image/tag/list",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert "data" in response.json()
    return response.json()["data"]