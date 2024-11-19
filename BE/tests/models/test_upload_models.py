import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from unittest.mock import AsyncMock
from services.project.upload_service import UploadService
from dto.uploads_dto import UploadRequest

@pytest.mark.asyncio
async def test_upload_image_success(test_maria_db, test_mongo_db):
    upload_service = UploadService(test_maria_db, test_mongo_db)
    upload_service._before_save_upload_batch = AsyncMock(return_value="mock_batch_id")
    upload_service._upload_s3 = AsyncMock(return_value={"urls": ["mock_url"], "labels": []})
    upload_service._analysis_data = AsyncMock()
    upload_service._after_save_upload_batch = AsyncMock()
    upload_service._mapping_user_upload_batches = AsyncMock()

    upload_request = UploadRequest(
        project_id="673a0c7899bc9b73f1f7b8de",
        is_private=False
    )
    files = [("test.jpg", b"file_content")]

    result = await upload_service.upload_image(upload_request, files, user_id=1)

    assert result == {"urls": ["mock_url"], "labels": []}
    upload_service._before_save_upload_batch.assert_called_once()
    upload_service._upload_s3.assert_called_once()
    upload_service._analysis_data.assert_called_once()
    upload_service._after_save_upload_batch.assert_called_once()
    upload_service._mapping_user_upload_batches.assert_called_once()

@pytest.mark.asyncio
async def test_upload_image_no_files(test_maria_db, test_mongo_db):
    upload_service = UploadService(test_maria_db, test_mongo_db)

    upload_request = UploadRequest(
        project_id="673a0c7899bc9b73f1f7b8de",
        is_private=False
    )
    files = []

    with pytest.raises(Exception, match="파일을 찾을 수 없습니다"):
        await upload_service.upload_image(upload_request, files, user_id=1)
