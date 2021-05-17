import re
from collections import defaultdict
from enum import Enum
from typing import Any, Dict, List, Union

from sqlalchemy import Column, table
from sqlalchemy.engine import RowProxy

JoinedRows = Dict[table, List[Dict[str, Any]]]
Row = Union[RowProxy, Dict[str, Union[Enum, Any]]]


def to_snake_case(string: str) -> str:
    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    string = re.sub("(.)([0-9]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", string).lower()


def row_proxy_to_dict(row: Row, keys_to_snake_case=True) -> Dict[str, Any]:
    return {to_snake_case(key) if keys_to_snake_case else key: value.value if isinstance(value, Enum) else value for key, value in row.items()}


def joined_rows_to_dict(rows: List[RowProxy], keys_to_snake_case: bool = True) -> JoinedRows:
    if not rows:
        return {}
    columns = {k: v for k, v in rows[0]._keymap.items() if isinstance(k, Column)}
    result = defaultdict(list)
    for i, row in enumerate(rows):
        for col, value in zip(columns, row):
            if len(result[col.table]) <= i:
                result[col.table].append({})
            result[col.table][i][col.name] = value

    return convert_joined_rows_to_snake_case(result) if keys_to_snake_case else result


def convert_joined_rows_to_snake_case(rows: JoinedRows) -> JoinedRows:
    result = rows.copy()
    for table_name, raw_rows in result.items():
        for i, row in enumerate(raw_rows):
            result[table_name][i] = {to_snake_case(k): v for k, v in row.items()}

    return result
