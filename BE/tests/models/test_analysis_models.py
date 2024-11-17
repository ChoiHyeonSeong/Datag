import pytest
from unittest.mock import AsyncMock, patch
from app.services.project.analysis_service import AnalysisService
from app.dto.analysis_dto import DimensionReductionRequest, AutoDimensionReductionRequest

@pytest.fixture
def analysis_service(test_maria_db, test_real_mongo_db):
    return AnalysisService(test_maria_db, test_real_mongo_db)

# 수동 차원축소 모델 테스트
@pytest.mark.asyncio
async def test_dimension_reduction_model(analysis_service):
    request = DimensionReductionRequest(
        project_id="67330084d4c23c34e7550e66",
        is_private=True,
        history_name="Manual Test",
        algorithm="tsne",
        image_ids=["67330084d4c23c34e7550e01"],
        selected_tags=[]
    )

    analysis_service._save_history_mongodb = AsyncMock(return_value="mocked_id")
    analysis_service._get_image_features = AsyncMock(return_value=[[0.1, 0.2, 0.3]])
    analysis_service._save_history_completed_mongodb = AsyncMock()

    response = await analysis_service.dimension_reduction(request, user_id=1)
    assert response.history_id == "mocked_id"

# 자동 차원축소 모델 테스트
@pytest.mark.asyncio
async def test_auto_dimension_reduction_model(analysis_service):
    request = AutoDimensionReductionRequest(
        project_id="67330084d4c23c34e7550e66",
        is_private=False,
        history_name="Auto Test",
        algorithm="umap",
        selected_tags=[]
    )

    analysis_service._save_history_mongodb = AsyncMock(return_value="mocked_id")
    analysis_service._get_image_features = AsyncMock(return_value=[[0.1, 0.2, 0.3]])
    analysis_service._save_history_completed_mongodb = AsyncMock()

    response = await analysis_service.auto_dimension_reduction(request, user_id=1)
    assert response.history_id == "mocked_id"

# 예외 처리 테스트
@pytest.mark.asyncio
async def test_dimension_reduction_model_failure(analysis_service):
    request = DimensionReductionRequest(
        project_id="67330084d4c23c34e7550e66",
        is_private=True,
        history_name="Failure Test",
        algorithm="tsne",
        image_ids=[],
        selected_tags=[]
    )

    with pytest.raises(Exception, match="Dimension reduction failed"):
        await analysis_service.dimension_reduction(request, user_id=1)
