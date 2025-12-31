from pydantic import BaseModel, Field
from typing import Literal


class VideoOut(BaseModel):
    platform: Literal["youtube", "bilibili", "twitch"]
    url: str
    title: str
    durationMs: int = Field(ge=0)
    thumbnailUrl: str
