from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from . import models
from .database import engine
from .routers import recruiter, jobs, seekers, apply
from . import auth

templates = Jinja2Templates(directory="app/templates")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(recruiter.router)
app.include_router(jobs.router)
app.include_router(seekers.router)
app.include_router(auth.router)
app.include_router(apply.router)


@app.get("/")
def home():
    return "Hello World!"
