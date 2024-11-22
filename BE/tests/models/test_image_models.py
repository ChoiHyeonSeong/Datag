import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from unittest.mock import AsyncMock
from services.image.image_service import ImageService
from dto.search_dto import SearchCondition
from dto.pagination_dto import PaginationDto

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
        SearchCondition(and_condition=[], or_condition=["dog"], not_condition=[])
    ]

    response = await image_service.search_images_by_conditions(search_conditions, user_id=1, page=1, limit=10)
    print(response.json())
    assert isinstance(response, PaginationDto)
    assert len(response.data) > 0

# 이미지 상세 정보 조회 모델 테스트
@pytest.mark.asyncio
async def test_read_image_detail(image_service):
    image_id = "673fda8c14cdfbe937b75019"

    response = await image_service.read_image_detail(user_id=1, image_id=image_id, search_conditions=[])
    print(response.json())
    assert response["metadata"]["_id"] == "673fda8b14cdfbe937b75016"
