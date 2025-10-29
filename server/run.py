from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.api.routes import router
from server.config import settings
from server.utils.logger import setup_logger

logger = setup_logger('fastapi_app')


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI application started")
    yield
    logger.info("FastAPI application shutting down")


app = FastAPI(
    title="Asset Correlation Analyzer API",
    description="API for analyzing correlations between financial assets",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api", tags=["correlations"])


@app.get("/")
async def root():
    return {"message": "Asset Correlation Analyzer API", "version": "1.0.0"}

