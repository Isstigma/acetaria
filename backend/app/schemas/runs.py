from decimal import Decimal
import uuid
from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from datetime import datetime
from app.schemas.media import VideoOut
from app.database.enums import ResultFlags, RunStatusEnum
from app.schemas.common import UnitModel

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

    # не обязательно for from_orm if you don't use ORM with MetricOut
    model_config = {"from_attributes": True}


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

    model_config = {"from_attributes": True}


class RunCostOut(BaseModel):
    cost_id: Optional[int] = None
    value: Optional[Decimal] = None

    model_config = {"from_attributes": True}


class UnitOut(UnitModel):
    id: Optional[int] = None

    model_config = {"from_attributes": True}


class TeamOut(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    units: Optional[List[UnitOut]] = None

    model_config = {"from_attributes": True}


class CharOut(BaseModel):
    id: Optional[int] = None
    name: str
    icon_url: Optional[str] = None
    rarity: int

    model_config = {"from_attributes": True}


class LightconeOut(BaseModel):
    id: Optional[int] = None
    name: str
    rarity: int
    icon_url: str
    sig_of_char_id: Optional[int] = None

    model_config = {"from_attributes": True}


class RunOut(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    team: TeamOut

    game_mode_entry_id: Optional[int] = None

    primary_score: Optional[Decimal] = None
    secondary_score: Optional[Decimal] = None
    flags: Optional[ResultFlags] = None

    author: Optional[str] = None
    link: Optional[str] = None
    name: Optional[str] = None
    submitted_at: Optional[datetime] = None

    status: Optional[RunStatusEnum] = None
    run_costs: list[RunCostOut] = []

    model_config = {"from_attributes": True}


class RunIn(BaseModel):
    stage_id: int
    author: Optional[str] = None
    link: str
    name: str
    primary_score: int
    secondary_score: Optional[int] = None
    units: list[UnitModel]
    flags: Optional[ResultFlags] = None
    submitted_by: Optional[str] = None


class CharFilterIn(BaseModel):  # todo, unused as of now
    id: Optional[int] = None
    eFrom: Optional[int] = None
    eTo: Optional[int] = None
    lcId: Optional[int] = None
    sFrom: Optional[int] = None
    sTo: Optional[int] = None
