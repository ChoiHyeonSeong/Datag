from fastapi import APIRouter, Depends, HTTPException, Security, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from sqlalchemy.orm import Session

from dto.analysis_dto import DimensionReductionRequest, AutoDimensionReductionRequest
from dto.common_dto import CommonResponse
from configs.mariadb import get_database_mariadb
from services.auth.auth_service import JWTManage
from services.project.analysis_service import AnalysisService

security_scheme = HTTPBearer()

router = APIRouter(prefix="/project", tags=["Project"])

@router.post("/analysis/manual", response_model=CommonResponse[dict])
async def dimension_reduction_umap(
    request: DimensionReductionRequest,
    background_tasks: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: Session = Depends(get_database_mariadb)
):
    try:
        if len(request.image_ids) < 10:
            raise HTTPException(status_code=400, detail="이미지 개수가 부족합니다. (최소 10개)")

        access_token = credentials.credentials
        jwt = JWTManage(db)
        user_id = jwt.verify_token(access_token)["user_id"]

        analysis_service = AnalysisService(db)
        background_tasks.add_task(
            analysis_service.dimension_reduction,
            request,
            user_id
        )
        
        return CommonResponse[dict](
            status=200,
            data={"message": "분석이 시작되었습니다. 잠시 후 결과를 확인할 수 있습니다."}
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/analysis/auto", response_model=CommonResponse[dict])
async def dimension_reduction_umap(
    request: AutoDimensionReductionRequest,
    background_tasks: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: Session = Depends(get_database_mariadb)
):
    try:
        access_token = credentials.credentials
        jwt = JWTManage(db)
        user_id = jwt.verify_token(access_token)["user_id"]

        analysis_service = AnalysisService(db)
        background_tasks.add_task(
            analysis_service.auto_dimension_reduction,
            request,
            user_id
        )
        
        return CommonResponse[dict](
            status=200,
            data={"message": "분석이 시작되었습니다. 잠시 후 결과를 확인할 수 있습니다."}
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))