from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import app.models
from app.models import Job
from app.schemas import JobCreate, JobResponse
from app.database import Base, engine, get_db
from app.routes.jobs import router as jobs_router


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

app.include_router(jobs_router)


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
    
app.include_router(jobs_router)