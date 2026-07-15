from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

import app.models
from app.models import Job
from app.schemas import JobCreate, JobResponse
from app.database import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="CareerPilot API",
    description="Backend API for the CareerPilot job search platform.",
    version="0.0.2",
    lifespan=lifespan,
)

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "CareerPilot is running"}

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}

@app.get("/health/database")
def database_health_check(
    database_session: Session = Depends(get_db),
) -> dict[str, str]:
    try:
        database_session.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }
    
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        ) from error
    
@app.post(
    "/jobs",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    job_data: JobCreate,
    database_session: Session = Depends(get_db),
) -> Job:
    job = Job(
        company=job_data.company,
        title=job_data.title,
        location=job_data.location,
        salary=job_data.salary,
        description=job_data.description,
        url=job_data.url,
    )

    database_session.add(job)

    try:
        database_session.commit()
        database_session.refresh(job)
        return job
    
    except IntegrityError as error:
        database_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A job with this url already exists",
        ) from error
    
@app.get(
    "/jobs",
    response_model=list[JobResponse],
)
def get_jobs(
    skip: int = 0,
    limit: int = 20,
    database_session: Session = Depends(get_db),
) -> list[Job]:
    statement = (
        select(Job)
        .order_by(Job.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    jobs = database_session.scalars(statement).all()

    return list(jobs)