from datetime import datetime
from decimal import Decimal
from enum import Enum, Flag, auto
import uuid
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Relationship, Session, UniqueConstraint, SQLModel, create_engine, select, text

from app.core.enums import GameModeKindEnum, ResultFlags, ResultKindEnum, VideoPlatformEnum

class Char (SQLModel, table=True):
  __tablename__ = "char"
  id: int | None = Field(default=None, primary_key=True, nullable=False)#todo recheck if id really shouldn't have | None with default=None
  name: str = Field(default=None, nullable=False)
  #path: todo
  icon_url: str | None = Field (default=None)
  rarity: int = Field(default=None, nullable=False)

  sig_lc: "Lightcone" = Relationship(back_populates="sig_of_char")

  units: list["Unit"] = Relationship(back_populates="char")

class Lightcone(SQLModel, table=True):
  __tablename__ = "lightcone"
  id: int | None = Field(default=None, primary_key=True, nullable=False)#todo recheck if id really shouldn't have | None with default=None
  name: str = Field(default=None, nullable=False)
  rarity: int = Field(default=None, nullable=True)
  icon_url: str = Field(default=None, nullable=False) 

  sig_of_char_id: int | None = Field(default=None, nullable=True, foreign_key="char.id")
  sig_of_char: Char | None = Relationship(back_populates="sig_lc")

  units: list["Unit"] = Relationship(back_populates="lc", )


class TeamUnitLink(SQLModel, table=True): 
  __tablename__ = "team_unit_link"
  team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
  unit_id: int | None = Field(default=None, foreign_key="unit.id", primary_key=True)


class Unit(SQLModel, table=True): #a single element of a team. 
  #In HSR - char with specific eidolon and optional lc with corresponding superimposition
  __tablename__ = "unit"
  __table_args__ = (UniqueConstraint("char_id", "char_eidolon", "lc_id", "lc_superimposition", name="unit_uidx"),)

  id: int | None = Field(default=None, primary_key=True)

  char_id: int | None = Field(default=None, nullable=False, foreign_key="char.id")
  char: Char | None = Relationship(back_populates="units")

  char_eidolon: int | None = Field(default=None, nullable=False)

  lc_id: int | None = Field(default=None, nullable=True, foreign_key="lightcone.id")
  lc: Lightcone | None = Relationship(back_populates="units")

  lc_superimposition: int | None = Field(default=None, nullable=True)

  teams: list["Team"] = Relationship(back_populates="units", link_model=TeamUnitLink)


class Team(SQLModel, table=True):
  __tablename__ = "team"
  id: int | None = Field(default=None, primary_key=True)
  name: str | None = Field(default=None, nullable=True)

  units: list["Unit"] | None = Relationship(back_populates="teams", link_model=TeamUnitLink)
  runs: list["Run"] | None = Relationship(back_populates="team")


#class GameMode serving as a template for each GMEntry needed with predefined ResultKindEnum and uhh idk some other settings
class GameMode(SQLModel, table=True):
  __tablename__ = "game_mode"

  id: int | None = Field(default=None, primary_key=True, nullable=False)
  #Installing alembic-postgresql-enum should achieve what you are looking for. https://pypi.org/project/alembic-postgresql-enum/
  kind: GameModeKindEnum | None = Field(default=None, unique=True, nullable=False)#^
  name: str | None = Field(default=None, nullable=False) 
  primary_score_kind: ResultKindEnum | None = Field(default=None, nullable=False) #in future it may be more than 2 and an additional relation will be needed
  primary_score_reverse_sorting: bool | None = Field(default=None, nullable=False)
  secondary_score_kind: ResultKindEnum | None = Field(default=None, nullable=True)
  secondary_score_reverse_sorting: bool | None = Field(default=None, nullable=False)

  game_mode_entries: list["GameModeEntry"] = Relationship(back_populates="game_mode")


class GameModeEntry(SQLModel, table=True): #specific boss in the specific rotation of a specific gamemode (e.g. 3.8 AA, knight 1)
  __tablename__ = "game_mode_entry"

  stage_id: int | None = Field(default=None, nullable=False, primary_key=True) #in-game id of a stage (either from MazeConfig or ChallengePeakConfig)
  
  name: str | None = Field(default=None, nullable=False)
  active_from: datetime | None = Field(default=None, nullable=False)
  active_to: datetime | None = Field(default=None, nullable=False)

  game_mode: GameMode | None = Relationship(back_populates="game_mode_entries")
  game_mode_id: int | None = Field(default=None, nullable=False, foreign_key="game_mode.id")

  runs: list["Run"] | None = Relationship(back_populates="game_mode_entry")


class Run(SQLModel, table=True):
  __tablename__ = "run"

  id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

  team: Team | None = Relationship(back_populates="runs")
  team_id: int | None = Field(default=None, nullable=False, foreign_key="team.id")
  
  game_mode_entry: GameModeEntry | None = Relationship(back_populates="runs")
  game_mode_entry_id: int | None = Field(default=None, nullable=False, foreign_key="game_mode_entry.stage_id")

  # primary_score: Decimal | None = Field(default=None, nullable=False, max_digits=8, decimal_places=3) #in future it may be more than 2 and an additional relation will be needed
  # secondary_score: Decimal | None = Field(default=None, nullable=True, max_digits=8, decimal_places=3)

  primary_score: int | None = Field(default=None, nullable=False) #in future it may be more than 2 and an additional relation will be needed
  secondary_score: int | None = Field(default=None, nullable=True)
  flags: ResultFlags | None = Field(default=None, nullable=True)
  
  author: str | None = Field(default=None, nullable=False)
  link: str | None = Field(default=None, nullable=False)
  name: str | None = Field(default=None, nullable=True)
  submitted_at: datetime | None = Field(default_factory=datetime.utcnow, nullable=False)

  run_costs: list["RunCost"] = Relationship(back_populates="run")

class Cost(SQLModel, table=True):
  __tablename__ = "cost"
  id: int | None = Field(default=None, primary_key=True, nullable=False)
  name: str | None = Field(default=None, nullable=False, unique=True)

  run_costs: list["RunCost"] = Relationship(back_populates="cost")
  #todo extend scoring, mb integrate with pvp balancing

class RunCost(SQLModel, table=True):
  __tablename__ = "run_cost"

  run: Run = Relationship(back_populates="run_costs")
  run_id: uuid.UUID | None = Field(default=None, nullable=False, foreign_key="run.id", primary_key=True)

  cost: Cost = Relationship(back_populates="run_costs")
  cost_id: int | None = Field(default=None, nullable=False, foreign_key="cost.id", primary_key=True)

  value: Decimal | None = Field(default=None, nullable=False)

class Submissions(SQLModel, table=True):
  __tablename__ = "submissions"

  link: str | None = Field(default=None, primary_key=True)
  submitted_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  description: str | None = Field(default=None, nullable=True)
# id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
# sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}