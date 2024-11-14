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

# 1. 해당 이미지 유저 권한 추가
def test_add_user_permission(auth_headers, mock_upload_service, mock_db):
    image_user_permission_add_request = {
    "image_id": "6732f4f3db3183653e78ac44",
    "user_id_list": [1, 2]
    }

    session = mongo_client.start_session()
    session.start_transaction()

    response = client.post(
        "be/api/image/permission/addUser",
        data={"image_user_permission_add_request": json.dumps(image_user_permission_add_request)},
        headers=auth_headers
    )

    session.abort_transaction()

    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": "해당 이미지에 유저 권한 추가를 성공하였습니다."
    }

    mock_upload_service.return_value.upload_image.assert_called_once()

# 2. 해당 이미지 유저 권한 삭제
def test_remove_user_permission(auth_headers, mock_upload_service, mock_db):
    image_user_permission_remove_request = {
    "image_id": "6732f4f3db3183653e78ac44",
    "user_id_list": [1, 2]
    }

    session = mongo_client.start_session()
    session.start_transaction()

    response = client.post(
        "be/api/image/permission/removeUser",
        data={"image_user_permission_remove_request": json.dumps(image_user_permission_remove_request)},
        headers=auth_headers
    )

    session.abort_transaction()

    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": "해당 이미지에 유저 권한 삭제를 성공하였습니다."
    }

    mock_upload_service.return_value.upload_image.assert_called_once()

# 3. 해당 이미지 부서 권한 추가
def test_add_department_permission(auth_headers, mock_upload_service, mock_db):
    image_department_permission_add_request = {
    "image_id": "6732f4f3db3183653e78ac44",
    "department_name_list": ["Research and Development", "Human Resource"]
    }

    session = mongo_client.start_session()
    session.start_transaction()

    response = client.post(
        "be/api/image/permission/addDepartment",
        data={"image_department_permission_add_request": json.dumps(image_department_permission_add_request)},
        headers=auth_headers
    )

    session.abort_transaction()

    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": "해당 이미지에 부서 권한 추가를 성공하였습니다"
    }

    mock_upload_service.return_value.upload_image.assert_called_once()

# 4. 해당 이미지 부서 권한 삭제
def test_remove_department_permission(auth_headers, mock_upload_service, mock_db):
    image_department_permission_remove_request = {
    "image_id": "6732f4f3db3183653e78ac44",
    "department_name_list": ["Research and Development", "Human Resource"]
    }

    session = mongo_client.start_session()
    session.start_transaction()

    response = client.post(
        "be/api/image/permission/removeDepartment",
        data={"image_department_permission_remove_request": json.dumps(image_department_permission_remove_request)},
        headers=auth_headers
    )

    session.abort_transaction()

    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": "해당 이미지에 부서 권한 삭제를 성공하였습니다"
    }

    mock_upload_service.return_value.upload_image.assert_called_once()

# 5. 이미지 정보 조회 (리퀘스트가 없으면 ??)
def test_get_image_detail(auth_headers, mock_upload_service, mock_db):
    image_department_permission_remove_request = {
    "image_id": "6732f4f3db3183653e78ac44"
    }

    session = mongo_client.start_session()
    session.start_transaction()

    response = client.post(
        "be/api/image/detail/{image_id}",
        data={"image_department_permission_remove_request": json.dumps(image_department_permission_remove_request)},
        headers=auth_headers
    )

    session.abort_transaction()

    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": "해당 이미지 정보 조회를 성공하였습니다"
    }

    mock_upload_service.return_value.upload_image.assert_called_once()

# 6. 해당 이미지에 태그 추가
def test_add_image_tag(auth_headers, mock_upload_service, mock_db):
    image_detail_tag_add_request = {
    "image_id": "6732f4f3db3183653e78ac44",
    "tag_list": ["dog", "bird"]
    }

    session = mongo_client.start_session()
    session.start_transaction()

    response = client.post(
        "be/api/image/tag/add",
        data={"image_detail_tag_add_request": json.dumps(image_detail_tag_add_request)},
        headers=auth_headers
    )

    session.abort_transaction()

    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": "해당 이미지에 유저 권한 추가를 성공하였습니다"
    }

    mock_upload_service.return_value.upload_image.assert_called_once()

# 7. 해당 이미지에 태그 삭제
def test_remove_image_tag(auth_headers, mock_upload_service, mock_db):
    image_detail_tag_remove_request = {
    "image_id": "6732f4f3db3183653e78ac44",
    "remove_tag_list": ["dog", "bird"]
    }
    
    session = mongo_client.start_session()
    session.start_transaction()

    response = client.post(
        "be/api/image/tag/remove",
        data={"image_detail_tag_remove_request": json.dumps(image_detail_tag_remove_request)},
        headers=auth_headers
    )

    session.abort_transaction()

    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": "이미지 업로드에 성공하였습니다."
    }

    mock_upload_service.return_value.upload_image.assert_called_once()