from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func

from app.database import get_db
from app.schemas import JobBase, JobOut, JobResponse
from app.oauth2 import get_current_user
from app.models import Jobs, JobsApplied


router = APIRouter(prefix="/job", tags=["Jobs"])


@router.post("/create", response_model=JobResponse)
def create_job(
    request: JobBase, db: Session = Depends(get_db), user_data=Depends(get_current_user)
):
    if user_data.get("role") != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    job = Jobs(**request.dict(), posted_by=user_data.get("id"))
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/all", response_model=List[JobOut])
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = (
        db.query(Jobs, func.count(JobsApplied.seeker_id).label("number_of_applicants"))
        .outerjoin(JobsApplied)
        .group_by(Jobs.id)
        .all()
    )
    return jobs


@router.get("/{id}", response_model=JobResponse)
def update_job(
    id: int,
    db: Session = Depends(get_db),
):
    job_query = db.query(Jobs).filter(id == Jobs.id)
    job = job_query.first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with the id:{id} does not exist",
        )
    return job


@router.put("/update/{id}")
def update_job(
    id: int,
    request: JobBase,
    db: Session = Depends(get_db),
    user_data=Depends(get_current_user),
):
    if user_data.get("role") != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    job_query = db.query(Jobs).filter(id == Jobs.id)
    job = job_query.first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with the id:{id} does not exist",
        )

    if job.posted_by != user_data.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    job_query.update(request.dict())
    db.commit()
    db.refresh(job)
    return job


@router.delete("/delete/{id}")
def delete_job(
    id: int,
    db: Session = Depends(get_db),
    user_data=Depends(get_current_user),
):
    if user_data.get("role") != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    job_query = db.query(Jobs).filter(id == Jobs.id)
    job = job_query.first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with the id:{id} does not exist",
        )

    if job.posted_by != user_data.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    job_query.delete()
    db.commit()
    return {"message": "Deleted Successfully"}
