from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm.session import Session

from starlette import status

from app.database import get_db
from app.models import Recruiters

from .config import settings

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
ACCESS_EXPIRE_MINUTES = settings.ACCESS_EXPIRE_MINUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def generate_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def verify_access_token(token, credential_exception):
    try:
        token_data = jwt.decode(token=token, algorithms=[ALGORITHM], key=SECRET_KEY)
        id = token_data.get("id")
        if id == None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid credentials",
        headers={"WWW-AUTHENTICATE": "BEARER"},
    )
    token_data = verify_access_token(token, credential_exception)
    # user = db.query(Recruiters).filter(Recruiters.id == token_data).first()
    return token_data
