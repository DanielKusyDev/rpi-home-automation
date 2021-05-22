import re
from enum import Enum
from typing import Any, Dict


def row_to_dict(row, keys_to_snake_case=True) -> Dict[str, Any]:
    def to_snake_case(string: str) -> str:
        string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
        string = re.sub("(.)([0-9]+)", r"\1_\2", string)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", string).lower()

    return {to_snake_case(key) if keys_to_snake_case else key: value.value if isinstance(value, Enum) else value for key, value in row.items()}
