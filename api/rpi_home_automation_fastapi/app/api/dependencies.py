from typing import Optional

from fastapi import Query

from app.config.settings import DEFAULT_PAGINATION_SIZE


class PaginationParams:
    def __init__(self, page: int = Query(default=1, gt=0), page_size: Optional[int] = DEFAULT_PAGINATION_SIZE):
        self.page = page
        self.page_size = page_size
