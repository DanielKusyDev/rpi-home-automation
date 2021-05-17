from typing import Iterable, Protocol

from app.core.entities.gpio import Gpio


class GpioRepo(Protocol):
    async def fetch_all(self) -> Iterable[Gpio]:
        ...
