import logging
import platform
import uuid
from configs.mongodb import mongo_url
from configs.mariadb import get_database_mariadb
from configs.s3 import upload_to_s3
from configs.mongodb import get_database_mongodb
from contextlib import asynccontextmanager
from routers.auth.auth_router import router as auth_router
from routers.department.department_router import router as department_router
from routers.image.image_router import router as image_router
from routers.image.permission_router import router as permission_router
from routers.image.tag_router import router as tag_router
from routers.project.analysis_router import router as analysis_router
from routers.project.base_router import router as base_router
from routers.project.history_router import router as history_router
from routers.user.user_router import router as user_router

import asyncio
from fastapi import FastAPI, APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(
    root_path="/be",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)


main_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins = [mongo_url, "*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

main_router.include_router(auth_router)
main_router.include_router(department_router)
main_router.include_router(image_router)
main_router.include_router(permission_router)
main_router.include_router(tag_router)
main_router.include_router(analysis_router)
main_router.include_router(base_router)
main_router.include_router(history_router)
main_router.include_router(user_router)

app.include_router(main_router)

@asynccontextmanager
async def startup_db_client(app: FastAPI):
    get_database_mongodb()
    get_database_mariadb()
    yield

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DB 연결 확인 엔드포인트
@app.get("/check-db-connection")
async def check_db_connection_mariadb(db: sessionmaker = Depends(get_database_mariadb)):
    try:
        # 간단한 쿼리 실행 (MariaDB 연결 확인)
        result = db.execute(text("SELECT 1"))
        return {"status": "connected", "result": result.fetchone()[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
    
# S3 연결 확인 엔드포인트
@app.post("/check-s3-connection")
async def check_db_connection_s3(file: UploadFile | None = File(None)):
    if not file:
        return {"image not found"}
    
    s3_filename = f"{uuid.uuid4()}.jpg"
    bucket_name = 'ssafy-project'
    upload_to_s3(file.file, bucket_name, s3_filename)
    
    s3_url = f"https://{bucket_name}.s3.us-east-2.amazonaws.com/{s3_filename}"

    return {"image_url" : s3_url}