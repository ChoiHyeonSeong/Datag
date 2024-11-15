from pydantic import BaseModel
from typing import List
from datetime import datetime

class Detection(BaseModel):
    prediction: str
    confidence: float
    threshold: float
    bbox: List[int]

class Prediction(BaseModel):
    fileIndex: int
    detections: List[Detection]
    inferenceStartedAt: datetime
    elapsedTime: float
    tags: List[str]

class AiResult(BaseModel):
    aiModel: str
    task: str
    predictions: List[Prediction]

class AccessControl(BaseModel):
    users: List[int]
    departments: List[str]
    projects: List[str]

class Metadata(BaseModel):
    branch: str
    process: str
    location: str
    equipmentId: str
    uploader: int
    isPrivate: bool
    accessControl: AccessControl
    createdAt: datetime
    mode: str

class AiResultData(BaseModel):
    schemaVersion: str = "1.0"
    fileList: List[str]
    metadata: Metadata
    aiResults: List[AiResult]