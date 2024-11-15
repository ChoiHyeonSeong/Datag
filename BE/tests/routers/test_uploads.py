import json
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from main import app
from configs.mongodb import client as mongo_client

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

@pytest.fixture
def mock_upload_service():
    with patch("app.services.project.upload_service.UploadService") as mock:
        yield mock

@pytest.fixture
def mock_db():
    return Mock()

# 1. 이미지 업로드 성공
def test_image_upload_success(auth_headers, mock_upload_service, mock_db):
    upload_request = {
    "project_id": "6732f477fcec9d2c66a7507c",
    "is_private": "false"
}
    files = [
        ("files", ("test1.jpg", b"file_content_1", "image/jpeg")),
        ("files", ("test2.jpg", b"file_content_2", "image/jpeg"))
    ]

    response = client.post(
        "be/api/project/image/upload",
        data={"upload_request": json.dumps(upload_request)},
        files=files,
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": "이미지 업로드에 성공하였습니다."
    }

    mock_upload_service.return_value.upload_image.assert_called_once()

# 2. files가 없는 경우
def test_image_upload_no_files(auth_headers, mock_upload_service, mock_db):
    upload_request = {
    "project_id": "67316151975201f5b1176329",
    "is_private": "false"
}

    response = client.post(
        "be/api/project/image/upload",
        data={"upload_request": json.dumps(upload_request)},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": "이미지 업로드에 성공하였습니다."
    }

    mock_upload_service.return_value.upload_image.assert_not_called()

# 3. token이 없는 경우
def test_image_upload_invalid_token(auth_headers, mock_db):

    upload_request = {
    "project_id": "67316151975201f5b1176329",
    "is_private": "false"
}
    files = []
    headers = {"Authorization": "Bearer invalid_token"}

    response = client.post(
        "be/api/project/image/upload",
        data={"upload_request": json.dumps(upload_request)},
        files=files,
        headers=headers
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "사용할 수 없는 토큰입니다."}

# 요청이 잘못된 경우
def test_image_upload_invalid_request(auth_headers, mock_db):
    invalid_upload_request = "invalid_json"

    response = client.post(
        "be/api/project/image/upload",
        data={"upload_request": invalid_upload_request},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert "detail" in response.json()