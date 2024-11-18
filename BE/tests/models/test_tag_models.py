import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
from app.main import app
from app.services.image.image_extra_service import ImageExtraService
from app.dto.image_detail_dto import (
    ImageDetailTagAddRequest,
    ImageDetailTagRemoveRequest,
    ImageUserPermissionAddRequest,
    ImageDepartmentPermissionAddRequest,
    ImageUserPermissionRemoveRequest,
    ImageDepartmentPermissionRemoveRequest
)

@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_service():
    with patch("app.services.image.image_extra_service.ImageExtraService") as mock:
        yield mock

# 태그 추가 테스트
@pytest.mark.asyncio
async def test_add_image_tag(mock_service, async_client):
    request_data = ImageDetailTagAddRequest(
        image_id="60b7c0ef9e1b2c001c8e4d3a",
        tag_list=["new_tag1", "new_tag2"]
    )
    
    mock_instance = mock_service.return_value
    mock_instance.add_image_tag = AsyncMock(return_value={"image_id": request_data.image_id, "tag_name_list": request_data.tag_list})

    response = await async_client.post(
        "/image/tag/add",
        json=request_data.dict()
    )

    assert response.status_code == 200, "태그 추가에 실패했습니다."
    assert response.json()["data"]["tag_name_list"] == request_data.tag_list
    mock_instance.add_image_tag.assert_called_once_with(request_data)

# 태그 삭제 테스트
@pytest.mark.asyncio
async def test_delete_image_tag(mock_service, async_client):
    request_data = ImageDetailTagRemoveRequest(
        image_id="60b7c0ef9e1b2c001c8e4d3a",
        remove_tag_list=["old_tag1", "old_tag2"]
    )
    
    mock_instance = mock_service.return_value
    mock_instance.delete_image_tag = AsyncMock(return_value={"image_id": request_data.image_id, "tag_name_list": []})

    response = await async_client.post(
        "/image/tag/remove",
        json=request_data.dict()
    )

    assert response.status_code == 200, "태그 삭제에 실패했습니다."
    assert "tag_name_list" in response.json()["data"]
    mock_instance.delete_image_tag.assert_called_once_with(request_data)

# 유저 권한 추가 테스트
@pytest.mark.asyncio
async def test_add_user_image_permission(mock_service, async_client):
    request_data = ImageUserPermissionAddRequest(
        image_id="60b7c0ef9e1b2c001c8e4d3a",
        user_id_list=["user1", "user2"]
    )
    
    mock_instance = mock_service.return_value
    mock_instance.add_user_image_permission = AsyncMock(return_value={"image_id": request_data.image_id, "auth_list": request_data.user_id_list})

    response = await async_client.post(
        "/image/permission/addUser",
        json=request_data.dict()
    )

    assert response.status_code == 200, "유저 권한 추가에 실패했습니다."
    assert "auth_list" in response.json()["data"]
    mock_instance.add_user_image_permission.assert_called_once_with(request_data)

# 부서 권한 추가 테스트
@pytest.mark.asyncio
async def test_add_department_image_permission(mock_service, async_client):
    request_data = ImageDepartmentPermissionAddRequest(
        image_id="60b7c0ef9e1b2c001c8e4d3a",
        department_name_list=["department1", "department2"]
    )
    
    mock_instance = mock_service.return_value
    mock_instance.add_department_image_permission = AsyncMock(return_value={"image_id": request_data.image_id, "department_list": request_data.department_name_list})

    response = await async_client.post(
        "/image/permission/addDepartment",
        json=request_data.dict()
    )

    assert response.status_code == 200, "부서 권한 추가에 실패했습니다."
    assert "department_list" in response.json()["data"]
    mock_instance.add_department_image_permission.assert_called_once_with(request_data)

# 유저 권한 삭제 테스트
@pytest.mark.asyncio
async def test_remove_user_image_permission(mock_service, async_client):
    request_data = ImageUserPermissionRemoveRequest(
        image_id="60b7c0ef9e1b2c001c8e4d3a",
        user_id_list=["user1", "user2"]
    )
    
    mock_instance = mock_service.return_value
    mock_instance.remove_user_image_permission = AsyncMock(return_value={"image_id": request_data.image_id, "auth_list": []})

    response = await async_client.post(
        "/image/permission/removeUser",
        json=request_data.dict()
    )

    assert response.status_code == 200, "유저 권한 삭제에 실패했습니다."
    assert "auth_list" in response.json()["data"]
    mock_instance.remove_user_image_permission.assert_called_once_with(request_data)

# 부서 권한 삭제 테스트
@pytest.mark.asyncio
async def test_remove_department_image_permission(mock_service, async_client):
    request_data = ImageDepartmentPermissionRemoveRequest(
        image_id="60b7c0ef9e1b2c001c8e4d3a",
        department_name_list=["department1", "department2"]
    )
    
    mock_instance = mock_service.return_value
    mock_instance.remove_department_image_permission = AsyncMock(return_value={"image_id": request_data.image_id, "department_list": []})

    response = await async_client.post(
        "/image/permission/removeDepartment",
        json=request_data.dict()
    )

    assert response.status_code == 200, "부서 권한 삭제에 실패했습니다."
    assert "department_list" in response.json()["data"]
    mock_instance.remove_department_image_permission.assert_called_once_with(request_data)
