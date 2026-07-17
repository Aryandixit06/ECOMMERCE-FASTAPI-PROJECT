from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool
    items: list[T]