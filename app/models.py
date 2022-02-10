from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Integer, String, Text
from .database import Base
from sqlalchemy import Column


class Recruiters(Base):
    __tablename__ = "recruiters"
    id = Column(Integer, nullable=False, index=True, primary_key=True)
    company = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    jobs = relationship("Jobs", back_populates="recruiter")


class Jobs(Base):
    __tablename__ = "jobs"
    id = Column(Integer, nullable=False, index=True, primary_key=True)
    title = Column(String, nullable=False)
    posted_by = Column(
        Integer,
        ForeignKey(column="recruiters.id", ondelete="CASCADE"),
    )
    post_time = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    eligibility_criteria = Column(String, nullable=False)
    job_location = Column(String, nullable=False)
    job_type = Column(String, nullable=False)
    level = Column(String, nullable=True)
    recruiter = relationship("Recruiters", back_populates="jobs")


class Seekers(Base):
    __tablename__ = "seekers"
    id = Column(Integer, nullable=False, index=True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    resume = Column(String, nullable=False)
    level = Column(String, nullable=False)
    portfolio = Column(String, nullable=True)
    job_feild = Column(String, nullable=False)


class JobsApplied(Base):
    __tablename__ = "jobs_applied"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    seeker_id = Column(
        Integer, ForeignKey("seekers.id", ondelete="CASCADE"), nullable=False
    )


class Selected_Candidates(Base):
    __tablename__ = "selected_candidates"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    seeker_id = Column(
        Integer, ForeignKey("seekers.id", ondelete="CASCADE"), nullable=False
    )
