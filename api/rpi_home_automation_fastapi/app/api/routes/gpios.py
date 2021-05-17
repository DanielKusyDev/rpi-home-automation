from typing import List

from app.api.container import get_dependencies
from app.core.entities.gpio import Gpio
from app.core.services import gpio_service
from fastapi import APIRouter
from starlette.responses import JSONResponse

repo = get_dependencies().gpio_repo
router = APIRouter(default_response_class=JSONResponse, prefix="/gpios")


@router.get("", response_model=List[Gpio], status_code=200)
async def get_all():
    return list(await gpio_service.get_all(repo))
