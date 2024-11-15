from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from sqlalchemy.orm import Session

from dto.pagination_dto import PaginationDto
from dto.history_dto import HistoryListData
from dto.common_dto import CommonResponse
from configs.mariadb import get_database_mariadb
from models.history_models import HistoryData
from services.auth.auth_service import JWTManage
from services.project.history_service import HistoryService

security_scheme = HTTPBearer()

router = APIRouter(prefix="/project/history", tags=["Project"])

@router.get("/{project_id}/list", response_model=CommonResponse[PaginationDto[List[HistoryListData]]])
async def get_history_list(
    project_id: str,
    page: int = 1,
    limit: int = 10,
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: Session = Depends(get_database_mariadb)
):
    try:
        access_token = credentials.credentials
        jwt = JWTManage(db)
        user_id = jwt.verify_token(access_token)["user_id"]

        history_service = HistoryService(db)
        results = await history_service.get_histories(project_id, user_id, page, limit)

        return CommonResponse[PaginationDto[List[HistoryListData]]](
            status=200,
            data=results
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/detail/{history_id}", response_model=CommonResponse[HistoryData])
async def get_history_detail(
    history_id: str,
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: Session = Depends(get_database_mariadb)
):
    try:
        history_service = HistoryService(db)
        results = await history_service.get_history_detail(history_id)

        return CommonResponse[HistoryData](
            status=200,
            data=results
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/delete/{history_id}", description="History 삭제")
async def delete_history(
    history_id: str,
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: Session = Depends(get_database_mariadb)
):
    try:
        history_service = HistoryService(db)
        await history_service.delete_history(history_id)

        return CommonResponse[str](
            status=200,
            data="History를 성공적으로 삭제하였습니다."
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))