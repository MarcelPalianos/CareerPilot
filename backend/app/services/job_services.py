from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job
from app.schemas import JobCreate, JobResponse, JobUpdate
from app.services.job_service import DuplicateJobUrlError, JobService


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
    try:
        return JobService.create_job(
            database_session=database_session,
            job_data=job_data,
        )
    except DuplicateJobUrlError as error:
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
    return JobService.get_jobs(
        database_session=database_session,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: int,
    database_session: Session = Depends(get_db),
) -> Job:
    job = JobService.get_job(
        database_session=database_session,
        job_id=job_id,
    )

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
    job = JobService.get_job(
        database_session=database_session,
        job_id=job_id,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    try:
        return JobService.update_job(
            database_session=database_session,
            job=job,
            job_data=job_data,
        )
    except DuplicateJobUrlError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A job with this URL already exists",
        ) from error