from typing import List
from bcrypt import re
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from fastapi.security import OAuth2PasswordRequestForm


from app.schemas import RecruiterBase, RecruiterResponse, RecruiterUpdate
from app.models import Jobs, JobsApplied, Recruiters, Seekers, Selected_Candidates
from app.database import get_db
from app.utils import hash, verify
from app.oauth2 import generate_access_token, get_current_user
from app.auth import login

router = APIRouter(prefix="/recruiter", tags=["Recruiters"])


@router.post("/create", response_model=RecruiterResponse)
def recruiter_signup(request: RecruiterBase, db: Session = Depends(get_db)):
    request.password = hash(request.password)
    recruiter = Recruiters(**request.dict())
    db.add(recruiter)
    db.commit()
    db.refresh(recruiter)
    return recruiter


@router.get("/all", response_model=List[RecruiterResponse])
def get_all_recruiters(db: Session = Depends(get_db)):
    recruiters = db.query(Recruiters).all()
    return recruiters


@router.get("/{id}", response_model=RecruiterResponse)
def get_recruiter(id: int, db: Session = Depends(get_db)):
    recruiter = db.query(Recruiters).filter(id == Recruiters.id).first()
    if not recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user with id:{id} Not found"
        )
    return recruiter


@router.put("/{id}", response_model=RecruiterResponse)
def update_recruiter(
    id: int,
    request: RecruiterUpdate,
    db: Session = Depends(get_db),
    user_data=Depends(get_current_user),
):
    if user_data.get("role") != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    if id != user_data.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    recruiter_query = db.query(Recruiters).filter(id == Recruiters.id)
    recruiter = recruiter_query.first()
    if not recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user with id:{id} Not found"
        )
    recruiter_query.update(request.dict())
    db.commit()
    db.refresh(recruiter)
    return recruiter


@router.delete("/{id}")
def delete_recruiter(
    id: int, db: Session = Depends(get_db), user_data=Depends(get_current_user)
):
    if user_data.get("role") != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    if id != user_data.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    recruiter_query = db.query(Recruiters).filter(id == Recruiters.id)
    recruiter = recruiter_query.first()
    if not recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id:{id} Not found"
        )
    recruiter_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Deleted Successfully"}


def recruiter_login(request, db):
    user = db.query(Recruiters).filter(request.username == Recruiters.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    if not verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = generate_access_token({"id": user.id, "role": "recruiter"})
    return {"access_token": token, "token_type": "bearer"}


@router.get("")
def dashboard(
    db: Session = Depends(get_db), user_data: dict = Depends(get_current_user)
):
    if user_data.get("role") != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    recruiter_query = (
        db.query(
            Recruiters.company,
            Jobs.title,
            Seekers.id,
            Seekers.name,
            Seekers.email,
        )
        .join(Jobs, isouter=True)
        .join(JobsApplied, isouter=True)
        .join(Seekers, isouter=True)
        .filter(Recruiters.id == user_data.get("id"))
        .all()
    )
    company = recruiter_query[0][0]
    for i in recruiter_query:
        print({"Title": i[1], "seeker_name": i[3], "seeker_email": i[4]})

    return recruiter_query


@router.post("/select/{job_id}/{seeker_id}")
def select_candidate(
    job_id: int,
    seeker_id: int,
    db: Session = Depends(get_db),
    user_data: dict = Depends(get_current_user),
):
    if user_data.get("role") != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    selected = Selected_Candidates(job_id=job_id, seeker_id=seeker_id)
    db.add(selected)
    db.commit()
    db.refresh(selected)
    return selected
