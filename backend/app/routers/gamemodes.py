from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.schemas.games import GameModeEntryOut, GameModeOut
from app.core.models import GameMode, GameModeEntry

router = APIRouter(tags=["gamemodes"])


@router.get("/games/{gameSlug}/modes", response_model=list[GameModeOut])
async def list_modes(gameSlug: str,
                     session: Session = Depends(get_session)
                     ):
    items = session.exec(select(GameMode)).all()
    # print(items[0])
    # for item in items:
    #   mode, entry = item
      # print(mode)
      # print(item[0])
      # print(item[1])
    return items

  # {'type': 'missing', 
  #  'loc': ('response', 479, 'secondary_score_kind'), 
  #  'msg': 'Field required', 
  #  'input': (GameMode(kind=<GameModeKindEnum.Aazz: 'Aazz'>, primary_score_kind=<ResultKindEnum.Av: 'Av'>, id=8, secondary_score_kind=None), 
  #             GameModeEntry(active_from=datetime.datetime(2026, 1, 5, 0, 0), name='PF 3.8 Ebon Deer', game_mode_id=2, stage_id=30318042, active_to=datetime.datetime(2026, 2, 16, 0, 0))
  #             )} 
  # (GameMode(primary_score_kind=<ResultKindEnum.Av: 'Av'>, kind=<GameModeKindEnum.Aazz: 'Aazz'>, secondary_score_kind=None, id=8), 
  #  GameModeEntry(active_from=datetime.datetime(2026, 1, 5, 0, 0), name='PF 3.8 Ebon Deer', 
  #  game_mode_id=2, stage_id=30318042, active_to=datetime.datetime(2026, 2, 16, 0, 0)))