from dataclasses import dataclass

from app.api.dependencies import PaginationParams


@dataclass
class Paginator:
    page: int
    page_size: int

    def __init__(self, params: PaginationParams):
        self.page = params.page
        self.page_size = params.page_size

    @property
    def skip(self):
        return self.page_size * (self.page - 1)

    @property
    def limit(self):
        return self.page_size + 1
