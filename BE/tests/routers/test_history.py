from fastapi import HTTPException
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock

from app.main import app
from app.services.project.history_service import HistoryService
from app.models.history_models import HistoryData
from app.dto.pagination_dto import PaginationDto
from app.dto.history_dto import HistoryListData

@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="module")
async def auth_headers(async_client):
    login_data = {
        "email": "test1@tmail.ws",  
        "password": "1234"
    }
    response = await async_client.post("be/api/auth/login", json=login_data)
    assert response.status_code == 200 
    token = response.json()["data"].get("access_token")
    assert token is not None, "토큰이 반환되지 않았습니다."
    return {"Authorization": f"Bearer {token}"}

# 히스토리 리스트 조회 성공
@pytest.mark.asyncio
async def test_get_history_list(async_client, auth_headers):

    project_id = "test_project_id"
    
    with patch.object(HistoryService, 'get_histories') as mock_get_histories:
        mock_get_histories.return_value = PaginationDto(
            data=[HistoryListData(id="1", title="Test History", created_at="2023-01-01")],
            page=1,
            limit=10,
            total_count=1
        )
        
        response = await async_client.get(f"/project/history/{project_id}/list?page=1&limit=10", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["status"] == 200
        assert len(response.json()["data"]["data"]) == 1
        assert response.json()["data"]["data"][0]["title"] == "Test History"

# 히스토리 상세 조회 성공
@pytest.mark.asyncio
async def test_get_history_detail(async_client, auth_headers):

    history_id = "test_history_id"
    
    with patch.object(HistoryService, 'get_history_detail') as mock_get_history_detail:
        mock_get_history_detail.return_value = HistoryData(
            id="1",
            title="Test History Detail",
            description="This is a test history detail",
            created_at="2023-01-01"
        )
        
        response = await async_client.get(f"/project/history/detail/{history_id}", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["status"] == 200
        assert response.json()["data"]["title"] == "Test History Detail"

# 히스토리 삭제 성공
@pytest.mark.asyncio
async def test_delete_history(async_client, auth_headers):

    history_id = "test_history_id"
    
    with patch.object(HistoryService, 'delete_history') as mock_delete_history:
        mock_delete_history.return_value = None
        
        response = await async_client.delete(f"/project/history/delete/{history_id}", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["status"] == 200
        assert response.json()["data"] == "History를 성공적으로 삭제하였습니다."

# 인증되지 않은 요청 처리
@pytest.mark.asyncio
async def test_get_history_list_unauthorized(async_client):

    project_id = "test_project_id"
    response = await async_client.get(f"/project/history/{project_id}/list?page=1&limit=10")
    assert response.status_code == 401  # Unauthorized

# 존재하지 않는 프로젝트에 대한 히스토리 리스트 조회
@pytest.mark.asyncio
async def test_get_history_list_not_found(async_client, auth_headers):

    project_id = "nonexistent_project_id"
    
    with patch.object(HistoryService, 'get_histories', side_effect=HTTPException(status_code=404, detail="Project not found")):
        response = await async_client.get(f"/project/history/{project_id}/list?page=1&limit=10", headers=auth_headers)
        assert response.status_code == 404
        assert "Project not found" in response.json()["detail"]

# 존재하지 않는 히스토리 삭제 시도
@pytest.mark.asyncio
async def test_delete_history_not_found(async_client, auth_headers):
    history_id = "nonexistent_history_id"
    
    with patch.object(HistoryService, 'delete_history', side_effect=HTTPException(status_code=404, detail="History not found")):
        response = await async_client.delete(f"/project/history/delete/{history_id}", headers=auth_headers)
        assert response.status_code == 404
        assert "History not found" in response.json()["detail"]