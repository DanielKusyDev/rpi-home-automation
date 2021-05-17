from dataclasses import dataclass
from typing import Callable, cast

from app.core.protocols.gpio_repo import GpioRepo
from app.core.protocols.plant_repo import PlantRepo
from app.core.protocols.sensor_repo import SensorRepo
from app.dao.repositories import (gpio_repository, plant_repository,
                                  sensor_repository)


@dataclass(frozen=True)
class Dependencies:
    plant_repo: PlantRepo
    sensor_repo: SensorRepo
    gpio_repo: GpioRepo


def _build_dependencies() -> Callable[[], Dependencies]:
    deps = Dependencies(
        plant_repo=cast(PlantRepo, plant_repository),
        sensor_repo=cast(SensorRepo, sensor_repository),
        gpio_repo=cast(GpioRepo, gpio_repository),
    )

    def fn() -> Dependencies:
        return deps

    return fn


get_dependencies = _build_dependencies()
