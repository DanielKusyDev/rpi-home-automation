from typing import List, Optional

from app.api.container import get_dependencies
from app.api.dependencies import PaginationParams
from app.api.errors import NotFound
from app.core.entities.common import Paginator
from app.core.entities.sensor import (Sensor, SensorInput, SensorsList,
                                      SensorType)
from app.core.services import sensor_service
from fastapi import APIRouter, Depends, Query, Request, Response
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter(prefix="/sensors")
repo = get_dependencies().sensor_repo


@router.get(path="/types", response_model=List[SensorType])
async def get_sensor_types():
    return list(await sensor_service.get_sensor_types(repo))


@router.get(path="", response_model=SensorsList)
async def get_all(
    request: Request,
    plant_ids: Optional[str] = Query(default=None, description="Comma separated list of plant ids"),
    pagination_params: PaginationParams = Depends(PaginationParams),
):
    paginator = Paginator(pagination_params)
    if plant_ids:
        sensors = list(await sensor_service.get_by_plants(repo, paginator, [int(id_) for id_ in plant_ids.split(",")]))
    else:
        sensors = list(await sensor_service.get_all(repo, paginator))
    return SensorsList.from_paginator(url=request.url, paginator=paginator, results=sensors)


@router.get(path="/{sensor_id}", response_model=Sensor)
async def get(sensor_id: int):
    try:
        return await sensor_service.get(repo, sensor_id)
    except NoResultFound:
        raise NotFound


@router.post("", response_model=Sensor)
async def create_one(request: Request, response: Response, sensor_dto: SensorInput):
    sensor_output = await sensor_service.create(repo, sensor_dto)
    response.headers["Location"] = request.url_for("get", sensor_id=sensor_output.id)
    return sensor_output


@router.put(path="/{sensor_id}", response_model=Sensor)
async def update(sensor_id: int, sensor_dto: SensorInput):
    return await sensor_service.update(repo, sensor_id, sensor_dto)
