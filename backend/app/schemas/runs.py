from decimal import Decimal
import uuid
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
from app.schemas.media import VideoOut
from app.core.enums import ResultFlags


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

    run_costs: list["RunCostOut"] 

class RunCostOut(BaseModel):
    cost_id: int | None 
    value: Decimal | None

class TeamOut(BaseModel):
    id: int | None 
    name: str | None 
    units: list["UnitOut"] | None

class UnitOut(BaseModel):
    id: int | None

    # char: "CharOut"
    char_id: int | None 
    char_eidolon: int | None

    lc_id: int | None
    # lc: "LightconeOut"
    lc_superimposition: int | None

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