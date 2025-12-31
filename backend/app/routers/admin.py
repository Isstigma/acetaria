from fastapi import APIRouter, Body

router = APIRouter(prefix="/admin", tags=["admin"])

# Auth/RBAC not implemented; endpoints exist for structure and return dummy success.


@router.post("/runs")
async def admin_create_run(payload: dict = Body(default={})):
    return {"ok": True, "runId": payload.get("runId", "run_dummy_created")}


@router.patch("/runs/{runId}")
async def admin_patch_run(runId: str, payload: dict = Body(default={})):
    return {"ok": True, "runId": runId, "patched": True, "payloadEcho": payload}


@router.post("/leaderboard-entries")
async def admin_create_leaderboard_entry(payload: dict = Body(default={})):
    return {"ok": True, "entryId": payload.get("entryId", "le_dummy_created")}


@router.patch("/leaderboard-entries/{entryId}")
async def admin_patch_leaderboard_entry(entryId: str, payload: dict = Body(default={})):
    return {"ok": True, "entryId": entryId, "patched": True, "payloadEcho": payload}


@router.post("/leaderboard-entries/{entryId}/teams")
async def admin_create_team_entry(entryId: str, payload: dict = Body(default={})):
    return {"ok": True, "entryId": entryId, "teamEntryId": payload.get("teamEntryId", "te_dummy_created")}


@router.patch("/team-entries/{teamEntryId}")
async def admin_patch_team_entry(teamEntryId: str, payload: dict = Body(default={})):
    return {"ok": True, "teamEntryId": teamEntryId, "patched": True, "payloadEcho": payload}
