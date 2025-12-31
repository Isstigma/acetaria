from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
from app.schemas.media import VideoOut


class MetricOut(BaseModel):
    type: Literal["cycles", "time"]
    cycles: Optional[int] = Field(default=None, ge=0)
    timeMs: Optional[int] = Field(default=None, ge=0)

    @staticmethod
    def cycles_metric(v: int) -> "MetricOut":
        return MetricOut(type="cycles", cycles=v, timeMs=None)

    @staticmethod
    def time_metric(v: int) -> "MetricOut":
        return MetricOut(type="time", cycles=None, timeMs=v)


class LatestRunCardOut(BaseModel):
    runId: str
    gameSlug: str
    gameName: str
    modeSlug: str
    modeName: str
    title: str
    place: int = Field(ge=1)
    metric: MetricOut
    playerName: str
    publishedAt: datetime
    video: VideoOut
