from typing import List, Optional

from app.core.entities import Model, PaginatedResponse


class SensorInput(Model):
    sensor_type_id: int
    description: Optional[str]
    plant_id: Optional[int]
    gpio_channel: Optional[int]


class Sensor(Model):
    id: int
    sensor_type_id: int
    description: Optional[str]
    plant_id: Optional[int]
    gpio_channel: Optional[int]
    state: Optional[bool]


class SensorsList(PaginatedResponse):
    results: List[Sensor]


class SensorType(Model):
    id: int
    name: str
