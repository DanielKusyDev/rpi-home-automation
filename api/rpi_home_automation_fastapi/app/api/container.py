from dataclasses import dataclass
from typing import Callable, cast

from app.adapters import weather_repository
from app.domain.weather_protocol import WeatherProtocol


@dataclass(frozen=True)
class Dependencies:
    weather_repo: WeatherProtocol


def _build_dependencies() -> Callable[[], Dependencies]:
    deps = Dependencies(
        weather_repo=cast(WeatherProtocol, weather_repository),
    )

    def fn() -> Dependencies:
        return deps

    return fn


get_dependencies = _build_dependencies()
