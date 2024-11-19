import pytest
from unittest.mock import patch, AsyncMock
from app.dto.image_detail_dto import ImageDetailTagAddRequest, ImageDetailTagRemoveRequest


# 태그 추가 테스트
@pytest.mark.asyncio
async def test_add_image_tag(async_client, auth_headers):
    request_data = ImageDetailTagAddRequest(
        image_id="60b7c0ef9e1b2c001c8e4d3a",
        tag_list=["new_tag1", "new_tag2"]
    )
    
    with patch("app.services.image.image_extra_service.ImageExtraService.add_image_tag", new_callable=AsyncMock) as mock_add_image_tag:
        mock_add_image_tag.return_value = {
            "image_id": request_data.image_id,
            "tag_name_list": request_data.tag_list
        }
        
        response = await async_client.post(
            "/image/tag/add",
            json=request_data.dict(),
            headers=auth_headers
        )

        assert response.status_code == 200, "태그 추가에 실패했습니다."
        assert "data" in response.json(), "응답 데이터가 없습니다."
        assert "tag_name_list" in response.json()["data"], "태그 목록이 포함되지 않았습니다."
        mock_add_image_tag.assert_called_once()

# 태그 삭제 테스트
@pytest.mark.asyncio
async def test_remove_image_tag(async_client, auth_headers):
    request_data = ImageDetailTagRemoveRequest(
        image_id="60b7c0ef9e1b2c001c8e4d3a",
        remove_tag_list=["new_tag1", "new_tag2"]
    )
    
    with patch("app.services.image.image_extra_service.ImageExtraService.delete_image_tag", new_callable=AsyncMock) as mock_delete_image_tag:
        mock_delete_image_tag.return_value = {
            "image_id": request_data.image_id,
            "tag_name_list": []
        }
        
        response = await async_client.post(
            "/image/tag/remove",
            json=request_data.dict(),
            headers=auth_headers
        )

        assert response.status_code == 200, "태그 삭제에 실패했습니다."
        assert "data" in response.json(), "응답 데이터가 없습니다."
        assert "tag_name_list" in response.json()["data"], "태그 목록이 포함되지 않았습니다."
        mock_delete_image_tag.assert_called_once()

# 태그 리스트 불러오기 테스트
@pytest.mark.asyncio
async def test_get_tags_and_images(async_client, auth_headers):
    with patch("app.services.image.image_service.ImageService.get_tag", new_callable=AsyncMock) as mock_get_tag:
        mock_get_tag.return_value = {
            "tags": ["existing_tag1", "existing_tag2"]
        }
        
        response = await async_client.get(
            "/image/tag/list",
            headers=auth_headers
        )

        assert response.status_code == 200, "태그 목록 불러오기에 실패했습니다."
        assert "data" in response.json(), "응답 데이터가 없습니다."
        assert "tags" in response.json()["data"], "태그 리스트가 포함되지 않았습니다."
        mock_get_tag.assert_called_once()
