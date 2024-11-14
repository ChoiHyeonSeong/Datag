from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from routers import cls_router, det_router
from services.mongodb.classification_metadata_service import ClassificationMetadataService
from services.mongodb.detection_metadata_service import ObjectDetectionMetadataService
from configs.mongodb import mongo_url
from configs.mongodb import get_database_mongodb
import traceback

app = FastAPI(
    root_path="/dl",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

main_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins = [mongo_url, "http://localhost:8000"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

main_router.include_router(cls_router.router)
main_router.include_router(det_router.router)

app.include_router(main_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, port=8001)
