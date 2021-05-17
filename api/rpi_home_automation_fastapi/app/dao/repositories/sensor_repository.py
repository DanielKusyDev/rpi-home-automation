from collections import defaultdict
from typing import Iterable, List, Optional

from app.core.entities.common import Paginator
from app.core.entities.sensor import Sensor, SensorInput, SensorType
from app.dao import database
from app.dao.models.gpio import gpio
from app.dao.models.sensors import sensor, sensor_type
from app.dao.utils import joined_rows_to_dict, row_proxy_to_dict
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.elements import BinaryExpression


def fetch_all(paginator: Paginator, filters: Optional[List[BinaryExpression]] = None) -> Iterable[Sensor]:
    query = select([sensor, gpio]).select_from(sensor.join(gpio)).limit(paginator.limit).offset(paginator.skip)
    if filters is not None:
        query = query.where(*filters)
    rows = database.execute(query).fetchall()
    if not rows:
        return []
    rows_as_dict = joined_rows_to_dict(rows)
    result = defaultdict(Sensor)
    for _sensor, _gpio in zip(rows_as_dict[sensor], rows_as_dict[gpio]):
        _id = _sensor["id"]
        result.setdefault(_id, Sensor.parse_obj({**_sensor, "state": _gpio["state"]}))
    return result.values()


async def fetch_sensor_types() -> Iterable[SensorType]:
    rows = database.execute(sensor_type.select()).fetchall()
    return (SensorType.parse_obj(row_proxy_to_dict(r)) for r in rows)


async def fetch_one(sensor_id: int) -> Sensor:
    query = select([sensor, gpio]).select_from(sensor.join(gpio)).where(sensor.c.Id == sensor_id)
    result = database.execute(query).fetchone()
    if not result:
        raise NoResultFound
    rows_as_dict = joined_rows_to_dict([result])
    return Sensor.parse_obj({**rows_as_dict[sensor][0], "state": rows_as_dict[gpio][0]["state"]})


async def persist(sensor_dto: SensorInput) -> Sensor:
    stmt = sensor.insert().values(**sensor_dto.pascal_case_dict()).returning(sensor.c.Id)
    result = database.execute(stmt).fetchone()
    return await fetch_one(result[sensor.c.Id])


async def update(sensor_id: int, sensor_dto: SensorInput) -> Sensor:
    stmt = sensor.update().where(sensor.c.Id == sensor_id).values(**sensor_dto.pascal_case_dict())
    database.execute(stmt)
    return await fetch_one(sensor_id)
