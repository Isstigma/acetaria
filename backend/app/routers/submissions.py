from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.session import get_session


router = APIRouter(tags=["submissions"])

# @router.post("/submissions")
# async def submit_run(
#   session: Session = Depends(get_session)
# ): 
#   pass

# @router.delete("/submissions/{submissionId}")
# async def reject_submission(
#   submissionId: str, 
#   session: Session = Depends(get_session)
# ):
#   pass

# @router.patch("/submissions/{submissionId}")
# async def approve_submission(
#   submissionId: str,
#   session: Session = Depends(get_session)
# ):
#   pass