from fastapi import APIRouter, HTTPException, Security, Depends, Query, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

from dto.common_dto import CommonResponse
from configs.mariadb import get_database_mariadb
from services.auth.auth_service import JWTManage
from services.image.image_service import ImageService
from services.image.download_service import DownloadService
from dto.search_dto import SearchRequest, ImageSearchResponse, SearchImageRequests
from dto.download_dto import DownloadRequest
from dto.pagination_dto import PaginationDto

security_scheme = HTTPBearer()

router = APIRouter(prefix="/image", tags=["Image"])

# 1. 이미지 정보 조회
@router.post('/detail', description="이미지 정보 조회")
async def get_image_detail(
    request : SearchImageRequests = Body(default=None),
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: Session = Depends(get_database_mariadb)
):
    try:
        image_service = ImageService(db)
        response = await image_service.read_image_detail(request.image_id, request.conditions)

        return CommonResponse(
            status=200,
            data=response
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/download")
async def download(
    request: DownloadRequest, 
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: Session = Depends(get_database_mariadb)
):
    try:
        download_service = DownloadService(db)
        return await download_service.download_image(request)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/search", response_model=CommonResponse[PaginationDto[List[ImageSearchResponse]]])
async def search_images(
    conditions: SearchRequest = Body(default=None),
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(10, ge=1, le=100, description="페이지당 항목 수"),
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: Session = Depends(get_database_mariadb)
):
    try:
        jwt = JWTManage(db)
        user_id = jwt.verify_token(credentials.credentials)["user_id"]
        
        conditions = conditions or SearchRequest()
        
        image_service = ImageService(db)
        result = await image_service.search_images_by_conditions(
            conditions.conditions, 
            user_id,
            page,
            limit
        )
        
        return CommonResponse(
            status=200,
            data=result
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
