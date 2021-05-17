from typing import Iterable

from app.core.entities.gpio import Gpio
from app.core.protocols.gpio_repo import GpioRepo


async def get_all(repo: GpioRepo) -> Iterable[Gpio]:
    return await repo.fetch_all()
