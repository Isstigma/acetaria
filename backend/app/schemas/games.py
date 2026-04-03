from datetime import datetime
from pydantic import BaseModel
from typing import Literal

from app.core.enums import GameModeKindEnum, ResultKindEnum


class GameOut(BaseModel):
    slug: str
    name: str

class GameModeOut(BaseModel):
  id: int | None 
  kind: GameModeKindEnum | None
  name: str | None
  primary_score_kind: ResultKindEnum | None
  primary_score_reverse_sorting: bool | None
  secondary_score_kind: ResultKindEnum | None
  secondary_score_reverse_sorting: bool | None
  game_mode_entries: list["GameModeEntryOut"]

class GameModeEntryOut(BaseModel):
  stage_id: int | None  #in-game id of a stage (either from MazeConfig or ChallengePeakConfig)
  
  name: str | None 
  active_from: datetime | None
  active_to: datetime | None

# class GameModeWithEntriesOut(BaseModel, GameModeOut, GameModeEntryOut):
#    {}