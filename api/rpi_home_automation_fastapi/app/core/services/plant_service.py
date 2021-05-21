from typing import Iterable

from app.api.routes.root import router as root_router
from app.api.routes.sensors import router as sensors_router
from app.config.settings import BASE_URL
from app.core.entities.common import Paginator
from app.core.entities.plant import Plant, PlantInput
from app.core.protocols.plant_repo import PlantRepo


def _get_plant_with_urls(plant: Plant):
    if plant.image:
        plant.image = BASE_URL + root_router.url_path_for("get_files", file_name=plant.image)
    plant.sensors = f"{BASE_URL}{sensors_router.url_path_for('get_all')}?plant_ids={plant.id}"
    return plant


async def get_all(repo: PlantRepo, paginator: Paginator) -> Iterable[Plant]:
    return (_get_plant_with_urls(_plant) for _plant in await repo.fetch_all(paginator))


async def get(repo: PlantRepo, plant_id: int) -> Plant:
    return _get_plant_with_urls(await repo.fetch_one(plant_id))


async def create(repo: PlantRepo, plant_dto: PlantInput) -> Plant:
    return _get_plant_with_urls(await repo.persist(plant_dto))


async def update(repo: PlantRepo, plant_id: int, plant_dto: PlantInput) -> Plant:
    return _get_plant_with_urls(await repo.update(plant_id, plant_dto))
