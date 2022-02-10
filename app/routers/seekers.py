from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

from app.database import get_db
from app.schemas import SeekerBase, SeekerResponse, SeekerUpdate
from app.models import Seekers
from app.oauth2 import generate_access_token, get_current_user
from app.utils import verify, hash


router = APIRouter(prefix="/seeker", tags=["Seekers"])


def seeker_login(request, db):
    user = db.query(Seekers).filter(request.username == Seekers.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    if not verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = generate_access_token({"id": user.id, "role": "seeker"})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/create", response_model=SeekerResponse)
def create_seeker(request: SeekerBase, db: Session = Depends(get_db)):
    request.password = hash(request.password)
    seeker = Seekers(**request.dict())
    db.add(seeker)
    db.commit()
    db.refresh(seeker)
    return seeker


@router.get("/all", response_model=List[SeekerResponse])
def get_all_seekers(db: Session = Depends(get_db)):
    seekers = db.query(Seekers).all()
    return seekers


@router.get("/{id}", response_model=SeekerResponse)
def get_seeker(id: int, db: Session = Depends(get_db)):
    seeker = db.query(Seekers).filter(Seekers.id == id).first()
    return seeker


@router.put("/{id}", response_model=SeekerResponse)
def update_seeker(
    id: int,
    request: SeekerUpdate,
    db: Session = Depends(get_db),
    user_data=Depends(get_current_user),
):
    if user_data.get("role") != "seeker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    if id != user_data.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    seeker_query = db.query(Seekers).filter(id == Seekers.id)
    seeker = seeker_query.first()
    if not seeker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} Does not exist",
        )
    seeker_query.update(request.dict())
    db.commit()
    db.refresh(seeker)
    return seeker


@router.delete("/{id}")
def update_seeker(
    id: int,
    db: Session = Depends(get_db),
    user_data=Depends(get_current_user),
):
    if user_data.get("role") != "seeker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    if id != user_data.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this action",
        )
    seeker_query = db.query(Seekers).filter(id == Seekers.id)
    seeker = seeker_query.first()
    if not seeker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} Does not exist",
        )
    seeker_query.delete()
    db.commit()
    return {"message": "Deleted Successfully!"}
