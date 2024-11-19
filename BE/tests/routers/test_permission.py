import pytest

# 부서 권한 추가 테스트
@pytest.mark.asyncio
async def test_add_department_permission(async_client, auth_headers):
    request_data = {
        "image_id": "67330084d4c23c34e7550e01",
        "department_id": "IT"
    }
    response = await async_client.post(
        "/be/api/image/permission/addDepartment",
        json=request_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == 200

# 사용자 권한 추가 테스트
@pytest.mark.asyncio
async def test_add_user_permission(async_client, auth_headers):
    request_data = {
        "image_id": "67330084d4c23c34e7550e01",
        "user_id": 123
    }
    response = await async_client.post(
        "/be/api/image/permission/addUser",
        json=request_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == 200

# 사용자 권한 삭제 테스트
@pytest.mark.asyncio
async def test_remove_user_permission(async_client, auth_headers):
    request_data = {
        "image_id": "67330084d4c23c34e7550e01",
        "user_id": 123
    }
    response = await async_client.post(
        "/be/api/image/permission/removeUser",
        json=request_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == 200

# 부서 권한 삭제 테스트
@pytest.mark.asyncio
async def test_remove_department_permission(async_client, auth_headers):
    request_data = {
        "image_id": "67330084d4c23c34e7550e01",
        "department_id": "IT"
    }
    response = await async_client.post(
        "/be/api/image/permission/removeDepartment",
        json=request_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == 200
