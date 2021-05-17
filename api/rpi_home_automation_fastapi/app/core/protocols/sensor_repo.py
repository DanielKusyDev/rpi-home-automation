from typing import Iterable, List, Optional, Protocol

from app.core.entities.common import Paginator
from app.core.entities.sensor import Sensor, SensorInput, SensorType
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList


class SensorRepo(Protocol):
    def fetch_all(self, paginator: Paginator, filters: Optional[List[BinaryExpression]] = None) -> Iterable[Sensor]:
        ...

    async def fetch_one(self, plant_id: int) -> Sensor:
        ...

    async def persist(self, plant_dto: SensorInput) -> Sensor:
        ...

    async def update(self, sensor_id: int, sensor_dto: SensorInput) -> Sensor:
        ...

    async def fetch_sensor_types(self) -> Iterable[SensorType]:
        ...
