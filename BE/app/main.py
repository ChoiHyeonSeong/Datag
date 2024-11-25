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
import logging
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(
    title="Backend API",
    description="Backend Service API",
    version="1.0.0",
    root_path="/be",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)     

main_router = APIRouter(prefix="/api")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins = [mongo_url, "*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.middleware("http")
async def db_session_middleware(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"MariaDB error: {str(e)}")
        raise

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