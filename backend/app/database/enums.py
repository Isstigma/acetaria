# TODO: enums will need to be rewritten in uppercase
from enum import Enum, Flag, StrEnum, auto

class GameModeKindEnum(StrEnum): 
  Unknown = "Unknown"
  Moc12 = "Moc12"
  Pf = "Pf"
  As = "As"
  Aak1 = "Aak1" #Knight 1
  Aak2 = "Aak2"
  Aak3 = "Aak3"
  Aacm = "Aacm" #lv100 CheckMate
  Aazz = "Aazz" #lv120 checkmate: ZugZwang

class ResultFlags(Flag):
  revive = auto()
  nohit = auto()

class RunStatusEnum(StrEnum):
  Pending = "Pending"
  Approved = "Approved"
  Rejected = "Rejected"

class VideoPlatformEnum(Enum):
  Bilibili = 1
  Youtube = 2
  Tiktok = 3
  Douyin = 4

class ResultKindEnum(StrEnum):
  Cycles = "Cycles"
  Av = "Av"
  Score = "Score"

class PathEnum(StrEnum):
  # None = 0
  Preservation = "Preservation"#1
  Remembrance = "Remembrance"#2
  Nihility = "Nihility"#3
  Abundance = "Abundance"#4
  TheHunt = "TheHunt"#5
  Destruction = "Destruction"#6
  Elation = "Elation"#7
  Harmony = "Harmony"#8
  Erudition = "Erudition"#9

class ElementEnum(StrEnum):
  # None=0
  Fire = "Fire"#1
  Ice = "Ice"#2
  Lightning = "Lightning"#3
  Wind = "Wind"#4
  Quantum = "Quantum"#5
  Imaginary = "Imaginary"#6
  Physical = "Physical"#7