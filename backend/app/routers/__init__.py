from .games import router as games_router
from .runs import router as runs_router
from .admin import router as admin_router
from .meta import router as meta_router
from .chars import router as chars_router
from .lightcones import router as lcs_router
from .gamemodes import router as gamemodes_router
from .costs import router as costs_router
from .submissions import router as submissions_router

ROUTERS = [
    games_router,
    runs_router,
    admin_router,
    meta_router,
    chars_router,
    lcs_router,
    gamemodes_router,
    costs_router,
    submissions_router,
]
