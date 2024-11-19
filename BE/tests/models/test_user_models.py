import pytest
from unittest.mock import MagicMock
from app.services.user.user_service import UserService
from app.models.mariadb_users import Users, Departments
from app.dto.users_dto import UserProfileUpdateRequest

@pytest.fixture
def user_service(test_maria_db):
    return UserService(test_maria_db)

# 프로필 조회 테스트
def test_get_profile(user_service):
    user_service._get_user_with_department = MagicMock(return_value=Users(
        user_id=1, name="John", email="john@example.com", department_id=1, is_supervised=False
    ))
    user_service.db.query = MagicMock()
    
    response = user_service.get_profile(1)
    assert response.name == "John"
    assert response.email == "john@example.com"

# 프로필 업데이트 테스트
def test_update_profile(user_service):
    user_service._get_user_with_department = MagicMock(return_value=Users(
        user_id=1, name="John", email="john@example.com", department_id=1, password="hashed_password", is_supervised=False
    ))
    user_service.pwd_context.verify = MagicMock(return_value=True)
    user_service.pwd_context.hash = MagicMock(return_value="new_hashed_password")
    user_service.db.commit = MagicMock()
    user_service.db.refresh = MagicMock()

    profile_update_request = UserProfileUpdateRequest(
        current_password="password",
        new_password="new_password",
        name="John Updated",
        duty="New Duty",
        department_id=2,
        location="New Location"
    )
    
    response = user_service.update_profile(1, profile_update_request)
    assert response.name == "John Updated"
    assert response.duty == "New Duty"
