from decimal import Decimal
import uuid
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
from app.schemas.media import VideoOut
from app.core.enums import ResultFlags, RunStatusEnum
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

class RunOut(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    team: "TeamOut" 

    game_mode_entry_id: int | None 

    primary_score: Decimal | None 
    secondary_score: Decimal | None 
    flags: ResultFlags | None 

    author: str | None 
    link: str | None 
    name: str | None 
    submitted_at: datetime | None

    status: RunStatusEnum | None
    run_costs: list["RunCostOut"] 

class RunIn(BaseModel):
  stage_id: int
  game_mode_entry_id: int | None
  author: str | None
  link: str
  name: str
  primary_score: int
  secondary_score: int | None
  units: list[UnitModel]
  flags: ResultFlags | None
  submitted_by: str | None
  submission_ref: str | None
  embed_discord: str | None #for some reason it is generated on frontend which is bullshit but w/e

class RunCostOut(BaseModel):
    cost_id: int | None 
    value: Decimal | None

class TeamOut(BaseModel):
    id: int | None 
    name: str | None 
    units: list["UnitOut"] | None

class UnitOut(UnitModel):
    id: int | None
    is_main: bool | None
    # char: "CharOut"

class CharOut(BaseModel):
    id: int | None
    name: str 
    icon_url: str | None 
    rarity: int 

class LightconeOut(BaseModel):
    id: int | None 
    name: str 
    rarity: int
    icon_url: str
    sig_of_char_id: int | None

class CharFilterIn(BaseModel): #todo, unused as of now
    id: int | None
    eFrom: int | None
    eTo: int | None
    lcId: int | None
    sFrom: int | None
    sTo: int | None