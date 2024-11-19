import pytest
from unittest.mock import AsyncMock
from app.services.image.image_service import ImageService
from app.dto.search_dto import SearchCondition, SearchRequest, ImageSearchResponse
from app.dto.pagination_dto import PaginationDto

@pytest.fixture
def image_service(test_maria_db, test_real_mongo_db):
    return ImageService(test_maria_db, test_real_mongo_db)

# 이미지 태그 조회 모델 테스트
@pytest.mark.asyncio
async def test_get_tag(image_service):
    image_service.collection_tag_images.find_one = AsyncMock(return_value={"tag": {"cat": ["1", "2"], "dog": ["3"]}})
    response = await image_service.get_tag()
    assert "cat" in response.tags
    assert "dog" in response.tags

# 이미지 조건 검색 모델 테스트
@pytest.mark.asyncio
async def test_search_images_by_conditions(image_service):
    search_conditions = [
        SearchCondition(and_condition=["cat"], or_condition=["dog"], not_condition=[])
    ]
    image_service._get_user_permissions = AsyncMock(return_value={"1", "2", "3"})
    image_service.collection_tag_images.find_one = AsyncMock(return_value={"tag": {"cat": ["1", "2"], "dog": ["3"]}})
    image_service.collection_images.find = AsyncMock(return_value=[{"_id": "1", "metadataId": "m1"}])
    image_service.collection_metadata.find = AsyncMock(return_value=[{"_id": "m1", "fileList": ["image_url"]}])

    response = await image_service.search_images_by_conditions(search_conditions, user_id=1, page=1, limit=10)
    assert isinstance(response, PaginationDto)
    assert len(response.data) > 0

# 이미지 상세 정보 조회 모델 테스트
@pytest.mark.asyncio
async def test_read_image_detail(image_service):
    image_id = "67330084d4c23c34e7550e01"
    image_service._get_user_permissions = AsyncMock(return_value={"67330084d4c23c34e7550e01"})
    image_service.collection_images.find_one = AsyncMock(return_value={"_id": image_id, "metadataId": "m1"})
    image_service.collection_metadata.find_one = AsyncMock(return_value={"_id": "m1", "metadata": {"accessControl": {"users": ["1"], "departments": ["IT"]}}})

    response = await image_service.read_image_detail(user_id=1, image_id=image_id, search_conditions=[])
    assert response["metadata"]["_id"] == "m1"
