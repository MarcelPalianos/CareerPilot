from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job
from app.schemas import JobCreate, JobResponse, JobUpdate


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
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
            detail="A job with this URL already exists",
        ) from error


@router.get(
    "",
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

@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: int,
    database_session: Session = Depends(get_db),
) -> Job:
    job = database_session.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return job

@router.patch(
    "/{job_id}",
    response_model=JobResponse,
)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    database_session: Session = Depends(get_db),
) -> Job:
    job = database_session.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    
    updates = job_data.model_dump(exclude_unset=False)

    for field, value in updates.items():
        setattr(job, field, value)

    try:
        database_session.commit()
        database_session.refresh(job)
        return job
    
    except IntegrityError as error:
        database_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A job with this URL already exists",
        ) from error