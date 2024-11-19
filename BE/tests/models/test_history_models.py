from fastapi import HTTPException
from unittest.mock import AsyncMock
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from app.services.project.history_service import HistoryService

@pytest.fixture
def history_service(test_maria_db, test_mongo_db):
    return HistoryService(test_maria_db, test_mongo_db)

# 히스토리 리스트 조회 모델 테스트
@pytest.mark.asyncio
async def test_get_histories_model(history_service):
    project_id = "67330084d4c23c34e7550e66"
    user_id = 1
    page = 1
    limit = 10

    history_service.collection_project_histories.find_one = AsyncMock(return_value={"project": {project_id: ["history_id_1"]}})
    history_service.collection_histories.find = AsyncMock(return_value=[{
        "_id": "history_id_1",
        "historyName": "Test History",
        "isDone": True,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T01:00:00Z"
    }])
    history_service.collection_histories.count_documents = AsyncMock(return_value=1)

    response = await history_service.get_histories(project_id, user_id, page, limit)
    assert response["total_count"] == 1
    assert len(response["data"]) == 1

# 히스토리 상세 조회 모델 테스트
@pytest.mark.asyncio
async def test_get_history_detail_model(history_service):
    history_id = "67359c084e4f42d16b01dc6a"
    history_service.collection_histories.find_one = AsyncMock(return_value={
        "_id": history_id,
        "historyName": "Test History Detail",
        "isDone": True,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T01:00:00Z"
    })

    response = await history_service.get_history_detail(history_id)
    assert response["_id"] == history_id

# 존재하지 않는 히스토리 삭제 모델 테스트
@pytest.mark.asyncio
async def test_delete_history_model(history_service):
    history_id = "nonexistent_history_id"
    history_service.collection_histories.find_one_and_delete = AsyncMock(return_value=None)

    with pytest.raises(HTTPException, match="History with id nonexistent_history_id not found"):
        await history_service.delete_history(history_id)
