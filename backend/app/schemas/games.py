from pydantic import BaseModel
from typing import Literal


class GameOut(BaseModel):
    slug: str
    name: str


class ModeOut(BaseModel):
    modeSlug: str
    modeName: str
    playMetricType: Literal["cycles", "time"]
    isLatest: bool
