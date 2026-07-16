from datetime import datetime

from pydantic import BaseModel, ConfigDict



class JobCreate(BaseModel):
    company: str
    title: str
    location: str
    salary: str
    description: str
    url: str


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    title: str
    location: str
    salary: str
    description: str
    url: str
    status: str
    created_at: datetime

class JobUpdate(BaseModel):
    company: str | None = None
    title: str | None = None
    location: str | None = None
    salary: str | None = None
    description: str | None = None
    url: str | None = None
    status: str | None = None