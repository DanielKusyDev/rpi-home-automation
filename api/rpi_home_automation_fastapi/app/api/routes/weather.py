from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from app.api.container import get_dependencies
from app.domain.weather_entities import Weather


repo = get_dependencies().weather_repo
router = APIRouter(default_response_class=JSONResponse)


@router.get(
    "/weather",
    response_model=Weather,
    status_code=status.HTTP_200_OK,
    summary="Checks the current weather",
)
def get_weather():
    return repo.fetch()
