from pydantic import BaseModel
from typing import Optional


class LightconeOut(BaseModel):
    id: int
    name: str
    path: Optional[str] = None
    icon_url: Optional[str] = None
    rarity: int
    sig_of_char_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }
