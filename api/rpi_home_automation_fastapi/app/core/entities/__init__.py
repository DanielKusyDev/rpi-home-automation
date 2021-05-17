import datetime
from typing import List, Optional

from app.core.entities.common import Paginator
from pydantic import BaseConfig, BaseModel, HttpUrl
from starlette.datastructures import URL


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(word if index == 0 else word.capitalize() for index, word in enumerate(string.split("_")))


class Model(BaseModel):
    class Config(BaseConfig):
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}
        allow_population_by_field_name = True
        alias_generator = convert_field_to_camel_case
        orm_mode = True

    def pascal_case_dict(self, **kwargs):
        data = self.dict(**kwargs)

        def transform_to_pascal_case(string: str):
            return string.replace("_", " ").title().replace(" ", "")

        return {transform_to_pascal_case(key): val for key, val in data.items()}


class PaginatedResponse(BaseModel):
    count: int
    results: List[BaseModel]
    next: Optional[HttpUrl]
    previous: Optional[HttpUrl]

    @classmethod
    def from_paginator(cls, url: URL, paginator: Paginator, results: List[BaseModel]):
        data = dict(results=results, count=len(results))
        if paginator.page - 1 > 0:
            data["previous"] = str(url.replace_query_params(page=paginator.page - 1, page_size=paginator.page_size))
        if len(results) >= paginator.page_size:
            data["next"] = str(url.replace_query_params(page=paginator.page + 1, page_size=paginator.page_size))
            data["results"] = results[:-1]
            data["count"] = max(len(results) - 1, 0)
        return PaginatedResponse(**data)
