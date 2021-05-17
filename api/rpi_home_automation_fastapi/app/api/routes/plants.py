from app.api.container import get_dependencies
from app.api.dependencies import PaginationParams
from app.api.errors import NotFound
from app.core.entities.common import Paginator
from app.core.entities.plant import Plant, PlantInput, PlantList
from app.core.services import plant_service
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm.exc import NoResultFound
from starlette.responses import JSONResponse

repo = get_dependencies().plant_repo
router = APIRouter(default_response_class=JSONResponse, prefix="/plants")


@router.get("", response_model=PlantList, status_code=200)
async def get_all(request: Request, pagination_params: PaginationParams = Depends(PaginationParams)):
    paginator = Paginator(pagination_params)
    plants = list(await plant_service.get_all(repo, paginator))
    return PlantList.from_paginator(url=request.url, paginator=paginator, results=plants)


@router.get(path="/{plant_id}", response_model=Plant)
async def get(plant_id: int):
    try:
        return await plant_service.get(repo, plant_id)
    except NoResultFound:
        raise NotFound


@router.post("", response_model=Plant, status_code=200)
async def create_one(
    request: Request,
    response: Response,
    plant_dto: PlantInput,
):
    plant_output = await plant_service.create(repo, plant_dto)
    response.headers["Location"] = request.url_for("get", plant_id=plant_output.id)
    return plant_output


@router.put(path="/{plant_id}", response_model=Plant)
async def update(plant_id: int, plant_dto: PlantInput):
    return await plant_service.update(repo, plant_id, plant_dto)
