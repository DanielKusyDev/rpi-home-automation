from dataclasses import dataclass
from typing import List

from app.core.entities import Model


@dataclass
class RepositoryResponse:
    rows: List[Model]
    all_rows_number: int
