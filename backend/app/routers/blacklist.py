from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.db import get_session
from app.core.models import SubmissionAuthorsBlacklist

router = APIRouter(prefix="/blacklist", tags=["blacklist"])

@router.post("/", response_model=SubmissionAuthorsBlacklist)
def create_blacklist(entry: SubmissionAuthorsBlacklist, session: Session = Depends(get_session)):
    session.add(entry)
    session.commit() 
    session.refresh(entry)
    return entry

@router.get("/", response_model=list[SubmissionAuthorsBlacklist])
def read_all_blacklist(session: Session = Depends(get_session)):
    return session.exec(select(SubmissionAuthorsBlacklist)).all()

@router.get("/{url}", response_model=SubmissionAuthorsBlacklist)
def read_blacklist(url: str, session: Session = Depends(get_session)):
    entry = session.get(SubmissionAuthorsBlacklist, url)
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    return entry

@router.patch("/{url}", response_model=SubmissionAuthorsBlacklist)
def update_blacklist(url: str, data: SubmissionAuthorsBlacklist, session: Session = Depends(get_session)):
    entry = session.get(SubmissionAuthorsBlacklist, url)
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    entry.reason = data.reason
    entry.name = data.name
    entry.blacklisted_by = data.blacklisted_by
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry

@router.delete("/{url}", status_code=204)
def delete_blacklist(url: str, session: Session = Depends(get_session)):
    entry = session.get(SubmissionAuthorsBlacklist, url)
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(entry)
    session.commit()