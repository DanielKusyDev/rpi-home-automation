from typing import Iterable, List

from app.core.entities.common import Paginator
from app.core.entities.sensor import Sensor, SensorInput, SensorType
from app.core.protocols.sensor_repo import SensorRepo
from app.dao.models.sensors import sensor


async def get_all(repo: SensorRepo, paginator: Paginator) -> Iterable[Sensor]:
    return repo.fetch_all(paginator)


async def get(repo: SensorRepo, plant_id: int) -> Sensor:
    return await repo.fetch_one(plant_id)


async def get_by_plants(repo: SensorRepo, paginator: Paginator, plant_ids: List[int]) -> Iterable[Sensor]:
    return repo.fetch_all(paginator=paginator, filters=[sensor.c.PlantId.in_(plant_ids)])


async def get_sensor_types(repo: SensorRepo) -> Iterable[SensorType]:
    return await repo.fetch_sensor_types()


async def create(repo: SensorRepo, plant_dto: SensorInput) -> Sensor:
    return await repo.persist(plant_dto)


async def update(repo: SensorRepo, sensor_id: int, sensor_dto: SensorInput) -> Sensor:
    return await repo.update(sensor_id, sensor_dto)
