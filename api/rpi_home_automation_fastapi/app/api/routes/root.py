import os
from enum import Enum

from app.api.errors import NotFound
from app.config import settings
from app.config.settings import MEDIA_ROOT
from fastapi import status
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field
from starlette.responses import FileResponse

router = APIRouter()


class StatusEnum(str, Enum):
    OK = "OK"
    FAILURE = "FAILURE"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class HealthCheck(BaseModel):
    title: str = Field(..., description="API title")
    status: StatusEnum = Field(..., description="API current status")


@router.get(
    "/status",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK,
    tags=["Health Check"],
    summary="Performs health check",
    description="Performs health check and returns information about running service.",
)
def health_check():
    return {
        "title": settings.PROJECT_NAME,
        "status": StatusEnum.OK,
    }


@router.get("/media/{file_name}", status_code=status.HTTP_200_OK, tags=["Static"])
async def get_files(file_name: str) -> FileResponse:
    path = os.path.join(MEDIA_ROOT, file_name)
    if not os.path.exists(path):
        raise NotFound
    return FileResponse(path)
