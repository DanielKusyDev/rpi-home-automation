from typing import Protocol

from app.domain.weather_entities import Weather


class WeatherProtocol(Protocol):
    def fetch(self) -> Weather:
        ...
