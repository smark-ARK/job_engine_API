from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
from sqlalchemy.orm.session import Session


from .routers import recruiter
from app.models import Recruiters, Seekers
from app.database import get_db
from app.routers import seekers


router = APIRouter(prefix="/login", tags=["AUTH"])


@router.post("")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    requester = (
        db.query(Recruiters).filter(Recruiters.email == request.username).first()
    )
    if not requester:
        token = seekers.seeker_login(request, db)
        return token
    token = recruiter.recruiter_login(request, db)
    return token
