import pytest
from unittest.mock import MagicMock, patch
from app.services.auth.auth_service import (
    UserCreate, EmailValidate, JWTManage, UserLogin, UserLogout, Permissions
)
from app.models.mariadb_users import Users
from app.dto.users_dto import UserSignUp, UserSignIn
from sqlalchemy.orm import Session

@pytest.fixture
def test_maria_db():
    # 세션을 모킹하여 사용합니다.
    return MagicMock(spec=Session)

@pytest.fixture
def user_create_service(test_maria_db):
    return UserCreate(test_maria_db)

@pytest.fixture
def email_validate_service(test_maria_db):
    mongodb_mock = MagicMock()
    return EmailValidate(test_maria_db, mongodb_mock)

@pytest.fixture
def jwt_manage_service(test_maria_db):
    return JWTManage(test_maria_db)

@pytest.fixture
def user_login_service(test_maria_db, jwt_manage_service):
    return UserLogin(test_maria_db, jwt_manage_service)

@pytest.fixture
def user_logout_service(test_maria_db):
    return UserLogout(test_maria_db)

# UserCreate 테스트
def test_create_temp_user(user_create_service):
    user_data = UserSignUp(
        email="test@example.com",
        password="password123",
        name="John Doe"
    )
    user_create_service._check_existing_email = MagicMock(return_value=False)
    
    temp_user_data = pytest.run(user_create_service.create_temp_user(user_data))
    assert "password" in temp_user_data
    assert user_create_service.pwd_context.verify("password123", temp_user_data["password"])

# EmailValidate 테스트
@pytest.mark.asyncio
async def test_send_verification_email(email_validate_service):
    temp_user_data = {"email": "test@example.com"}
    with patch.object(email_validate_service, "_send_email") as mock_send_email, patch.object(email_validate_service, "_store_verification_data") as mock_store_data:
        mock_send_email.return_value = None
        mock_store_data.return_value = None

        code = await email_validate_service.send_verification_email("test@example.com", temp_user_data)
        assert len(code) > 0  # 코드가 생성되었는지 확인

# JWTManage 테스트
def test_create_access_token(jwt_manage_service):
    user = Users(user_id=1, email="test@example.com")
    token = jwt_manage_service.create_access_token(user)
    assert token is not None

def test_verify_token(jwt_manage_service):
    user = Users(user_id=1, email="test@example.com")
    token = jwt_manage_service.create_access_token(user)
    payload = jwt_manage_service.verify_token(token)
    assert payload["user_id"] == 1

# UserLogin 테스트
@pytest.mark.asyncio
async def test_login(user_login_service):
    user_login_service.db.query = MagicMock()
    user = Users(user_id=1, email="test@example.com", password=user_login_service.pwd_context.hash("password123"))
    user_login_service.db.query().filter().first.return_value = user
    
    login_data = UserSignIn(email="test@example.com", password="password123")
    token_response = await user_login_service.login(login_data)
    assert "access_token" in token_response.model_dump()
    assert "refresh_token" in token_response.model_dump()

# UserLogout 테스트
@pytest.mark.asyncio
async def test_logout(user_logout_service, jwt_manage_service):
    token = jwt_manage_service.create_access_token(Users(user_id=1, email="test@example.com"))
    response = await user_logout_service.logout(token)
    assert response["message"] == "로그아웃 되었습니다"
