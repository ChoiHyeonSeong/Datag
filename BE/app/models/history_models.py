from pydantic import BaseModel
from typing import List, Any
from datetime import datetime
from dto.search_dto import SearchCondition

class Parameters(BaseModel):
    selectedAlgorithm: str
    selectedTags: List[SearchCondition]

class ReductionResults(BaseModel):
    imageId: str
    imageUrl: str
    features: List[float]
    predictions: Any
    label: Any

class HistoryData(BaseModel):
    userId: int
    projectId: str
    isPrivate: bool
    historyName: str
    isDone: bool
    parameters: Parameters | None = None
    results: List[ReductionResults] | None = None
    createdAt: datetime
    updatedAt: datetime