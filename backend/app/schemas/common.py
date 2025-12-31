from pydantic import BaseModel, Field
from typing import Generic, List, TypeVar

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: List[T]
    page: int = Field(ge=1)
    pageSize: int = Field(ge=1, le=200)
    total: int = Field(ge=0)
