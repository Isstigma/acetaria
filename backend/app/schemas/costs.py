from pydantic import BaseModel
from typing import Dict


class CostOut(BaseModel): 
    id: int | None 
    name: str | None

class FreeCharactersResponse(BaseModel):
    limits: dict[str, int]
    selector_pool: list[str]
    selector_limit: int