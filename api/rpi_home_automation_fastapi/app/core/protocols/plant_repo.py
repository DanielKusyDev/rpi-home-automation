from typing import Iterable, Protocol

from app.core.entities.common import Paginator
from app.core.entities.plant import Plant, PlantInput


class PlantRepo(Protocol):
    async def fetch_all(self, paginator: Paginator) -> Iterable[Plant]:
        ...

    async def fetch_one(self, plant_id: int) -> Plant:
        ...

    async def persist(self, plant_dto: PlantInput) -> Plant:
        ...

    async def update(self, plant_id: int, plant_dto: PlantInput) -> Plant:
        ...
