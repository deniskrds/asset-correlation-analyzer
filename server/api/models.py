from datetime import datetime, UTC
from typing import Dict, List
from typing import TypeVar, Generic, Optional

from pydantic import BaseModel, Field

T = TypeVar('T')


class BaseResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: str
    status_code: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CorrelationResponse(BaseModel):
    correlation_matrix: Dict[str, Dict[str, float]]
    assets: List[str]
    data_points: int
