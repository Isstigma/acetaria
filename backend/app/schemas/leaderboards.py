from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.runs import MetricOut
from app.schemas.media import VideoOut


class CharacterOut(BaseModel):
    id: str
    name: str
    portraitUrl: str


class PlayerOut(BaseModel):
    displayName: str


class TeamMemberPortraitOut(BaseModel):
    id: str
    portraitUrl: str


class LeaderboardEntryOut(BaseModel):
    entryId: str
    character: CharacterOut
    limStd: int = Field(ge=0)
    metric: MetricOut
    player: PlayerOut
    # Optional rank fields for future (frontend should not show in leaderboard table)
    rank: Optional[int] = None


class TeamEntryOut(BaseModel):
    teamEntryId: str
    team: List[TeamMemberPortraitOut] = Field(min_length=4, max_length=4)
    limStd: int = Field(ge=0)
    metric: MetricOut
    player: PlayerOut
    video: VideoOut
