from os import ST_SYNCHRONOUS
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from app.database import get_db
from app.oauth2 import get_current_user
from app.models import JobsApplied

router = APIRouter(prefix="/apply", tags=["Apply job"])


@router.post("/{id}")
def apply_job(
    id: int, db: Session = Depends(get_db), applicant=Depends(get_current_user)
):
    if applicant.get("role") != "seeker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    applied = JobsApplied(job_id=id, seeker_id=applicant.get("id"))
    db.add(applied)
    db.commit()
    return {"message": "Applied Successfully!"}
