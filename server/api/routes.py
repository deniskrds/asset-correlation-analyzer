from fastapi import APIRouter

from server.api.service import get_correlation_matrix
from server.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger('correlation_api')


@router.get("/correlations")
async def get_correlations():
    response = get_correlation_matrix()
    return response.model_dump()


@router.get("/health")
async def health_check():
    return {"status": "healthy"}
