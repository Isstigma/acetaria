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

class VideoPlatformEnum(Enum):
  Bilibili = 1
  Youtube = 2
  Tiktok = 3
  Douyin = 4

class ResultKindEnum(StrEnum):
  Cycles = "Cycles"
  Av = "Av"
  Score = "Score"