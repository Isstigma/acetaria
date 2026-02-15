from pydantic import BaseModel
from typing import Optional

class CharOut(BaseModel):
    id: int
    name: str
    path: str
    element: str
    icon_url: Optional[str] = None
    rarity: int

    model_config = {
        "from_attributes": True
    }
