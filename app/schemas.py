from datetime import datetime
from typing import List
from pydantic import BaseModel
from pydantic.networks import EmailStr

# Recruiter start
class RecruiterBase(BaseModel):
    company: str
    email: EmailStr
    password: str


class RecruiterUpdate(BaseModel):
    company: str
    email: EmailStr


class JobRecruiters(BaseModel):
    id: int
    title: str
    posted_by: int
    post_time: datetime
    eligibility_criteria: str
    job_location: str
    job_type: str
    level: str

    class Config:
        orm_mode = True


class RecruiterResponse(BaseModel):
    id: int
    company: str
    email: EmailStr
    jobs: List[JobRecruiters]

    class Config:
        orm_mode = True


# Recruiter End

# Jobs Start


class JobBase(BaseModel):
    title: str
    eligibility_criteria: str
    job_location: str
    job_type: str
    level: str


class RecruiterJobs(BaseModel):
    id: int
    company: str
    email: EmailStr

    class Config:
        orm_mode = True


class JobResponse(BaseModel):
    id: int
    title: str
    posted_by: int
    post_time: datetime
    eligibility_criteria: str
    job_location: str
    job_type: str
    level: str
    recruiter: RecruiterJobs

    class Config:
        orm_mode = True


class JobOut(BaseModel):
    Jobs: JobResponse
    number_of_applicants: int

    class Config:
        orm_mode = True


# Jobs End
# Seekers Start
class SeekerBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    resume: str
    level: str
    portfolio: str
    job_feild: str


class SeekerUpdate(BaseModel):
    name: str
    email: EmailStr
    resume: str
    level: str
    portfolio: str
    job_feild: str


class SeekerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    resume: str
    level: str
    portfolio: str
    job_feild: str

    class Config:
        orm_mode = True
