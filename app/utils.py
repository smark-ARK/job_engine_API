from passlib import context
from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(plain):
    return context.hash(plain)


def verify(plain, hashed):
    return context.verify(plain, hashed)
