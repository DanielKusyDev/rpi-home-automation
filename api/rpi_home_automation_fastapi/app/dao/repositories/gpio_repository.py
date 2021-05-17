from typing import Iterable

from app.core.entities.gpio import Gpio
from app.dao import database
from app.dao.models.gpio import gpio
from app.dao.utils import row_proxy_to_dict


async def fetch_all() -> Iterable[Gpio]:
    result = database.execute(gpio.select()).fetchall()
    return (Gpio.parse_obj(row_proxy_to_dict(r)) for r in result)
