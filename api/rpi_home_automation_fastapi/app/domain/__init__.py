import datetime
from dataclasses import dataclass

from pydantic import BaseConfig, BaseModel


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(word if index == 0 else word.capitalize() for index, word in enumerate(string.split("_")))


class Entity(BaseModel):
    class Config(BaseConfig):
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}
        allow_population_by_field_name = True
        alias_generator = convert_field_to_camel_case

    def pascal_case_dict(self, **kwargs):
        data = self.dict(**kwargs)

        def transform_to_pascal_case(string: str):
            return string.replace("_", " ").title().replace(" ", "")

        return {transform_to_pascal_case(key): val for key, val in data.items()}
