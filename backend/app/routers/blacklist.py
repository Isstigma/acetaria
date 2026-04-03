from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import require_admin, require_moderator_or_admin
from app.core.db import get_session
from app.core.models import SubmissionAuthorsBlacklist, User

router = APIRouter(prefix="/blacklist", tags=["blacklist"])


@router.post("/", response_model=SubmissionAuthorsBlacklist)
async def create_blacklist(
    entry: SubmissionAuthorsBlacklist,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin),
):
    entry.blacklisted_by = current_user.id
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


@router.get("/", response_model=list[SubmissionAuthorsBlacklist])
async def read_all_blacklist(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_moderator_or_admin),
):
    return (await session.execute(select(SubmissionAuthorsBlacklist))).scalars().all()


@router.get("/{url}", response_model=SubmissionAuthorsBlacklist)
async def read_blacklist(
    url: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin),
):
    entry = await session.get(SubmissionAuthorsBlacklist, url)
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    return entry


@router.patch("/{url}", response_model=SubmissionAuthorsBlacklist)
async def update_blacklist(
    url: str,
    data: SubmissionAuthorsBlacklist,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin),
):
    entry = await session.get(SubmissionAuthorsBlacklist, url)
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    entry.reason = data.reason
    entry.name = data.name
    entry.blacklisted_by = current_user.id
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


@router.delete("/{url}", status_code=204)
async def delete_blacklist(
    url: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin),
):
    entry = await session.get(SubmissionAuthorsBlacklist, url)
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    await session.delete(entry)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
