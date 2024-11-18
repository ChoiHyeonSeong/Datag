import pytest
from unittest.mock import MagicMock
from app.services.auth.auth_service import Permissions
from app.models.mariadb_users import Users

@pytest.fixture
def permissions_service(test_maria_db):
    mongodb_mock = MagicMock()
    return Permissions(test_maria_db, mongodb_mock)

# Permissions 테스트
@pytest.mark.asyncio
async def test_get_image_permissions(permissions_service):
    permissions_service.db.query().filter().first.return_value = Users(user_id=1, department_id=1)
    permissions_service.collection_image_permissions.find_one.return_value = {
        "user": {"1": ["image1", "image2"]},
        "department": {"IT": ["image3", "image4"]}
    }

    image_ids = await permissions_service.get_image_permissions(1)
    assert "image1" in image_ids
    assert "image2" in image_ids