import pytest
from services.image.download_service import DownloadService
from dto.download_dto import DownloadRequest
from fastapi import HTTPException
from bson import ObjectId
import asyncio

# 다운로드 요청 시 메타데이터 가져오기 성공
@pytest.mark.asyncio
async def test_get_metadata_success(test_real_mongo_db, event_loop):
    download_service = DownloadService(None, test_real_mongo_db)
    metadata_id = "6732f4f3db3183653e78ac41"
    
    asyncio.set_event_loop(event_loop) 
    
    metadata = await download_service.get_metadata(metadata_id)
    assert metadata["_id"] == metadata_id

# 다운로드 요청 시 메타데이터 가져오기 실패
@pytest.mark.asyncio
async def test_get_metadata_not_found(test_real_mongo_db, event_loop):
    download_service = DownloadService(None, test_real_mongo_db)
    invalid_metadata_id = "000000000000000000000000"
    
    asyncio.set_event_loop(event_loop) 
    
    with pytest.raises(HTTPException) as exc_info:
        await download_service.get_metadata(invalid_metadata_id)
    
    assert "메타데이터를 가져오는 중 오류 발생" in str(exc_info.value)

# 다운로드 요청 시 피처 가져오기 성공
@pytest.mark.asyncio
async def test_get_feature_success(test_real_mongo_db, event_loop):
    download_service = DownloadService(None, test_real_mongo_db)
    feature_id = "6732f4f5db3183653e78ac49"
    
    asyncio.set_event_loop(event_loop) 
    
    feature = await download_service.get_feature(feature_id)
    assert feature["_id"] == feature_id

# 다운로드 요청 시 피처 가져오기 실패
@pytest.mark.asyncio
async def test_get_feature_not_found(test_real_mongo_db, event_loop):
    download_service = DownloadService(None, test_real_mongo_db)
    invalid_feature_id = "000000000000000000000000"
    
    asyncio.set_event_loop(event_loop) 
    
    with pytest.raises(HTTPException) as exc_info:
        await download_service.get_feature(invalid_feature_id)
    
    assert "피처 데이터를 가져오는 중 오류 발생" in str(exc_info.value)

# 이미지 다운로드 시 성공
@pytest.mark.asyncio
async def test_download_image_success(test_real_mongo_db, event_loop):
    download_service = DownloadService(None, test_real_mongo_db)
    download_request = DownloadRequest(image_list=["6737051e74be3f50d27e2cde"])
    
    asyncio.set_event_loop(event_loop) 
    
    response = await download_service.download_image(download_request)
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment; filename=")
