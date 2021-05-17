from typing import Any, Dict, Iterable

from app.core.entities.common import Paginator
from app.core.entities.plant import Plant, PlantInput
from app.core.services.files_service import save_base64_encoded_file
from app.dao import database
from app.dao.models.plants import plant
from app.dao.utils import row_proxy_to_dict
from sqlalchemy.orm.exc import NoResultFound


def _get_data_to_insert(plant_dto: PlantInput) -> Dict[str, Any]:
    data = plant_dto.pascal_case_dict()
    if data.pop("EncodedImage", None):
        _, file_name = save_base64_encoded_file(plant_dto.encoded_image, "jpg")
        data["Image"] = file_name
    return data


async def fetch_all(paginator: Paginator) -> Iterable[Plant]:
    query = plant.select().limit(paginator.limit).offset(paginator.skip).order_by(plant.c.Id)
    rows = database.execute(query).fetchall()
    if not rows:
        return []
    return (Plant(**row_proxy_to_dict(row)) for row in rows)


async def fetch_one(plant_id: int) -> Plant:
    result = database.execute(plant.select().where(plant.c.Id == plant_id)).fetchone()
    if not result:
        raise NoResultFound
    return Plant(**row_proxy_to_dict(result))


async def persist(plant_dto: PlantInput) -> Plant:
    stmt = plant.insert().values(**_get_data_to_insert(plant_dto)).returning(plant.c.Id)
    result = database.execute(stmt).fetchone()
    return await fetch_one(result[plant.c.Id])


async def update(plant_id: int, plant_dto: PlantInput) -> Plant:
    stmt = plant.update().where(plant.c.Id == plant_id).values(**_get_data_to_insert(plant_dto))
    database.execute(stmt)
    return await fetch_one(plant_id)
