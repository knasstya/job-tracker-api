from datetime import datetime
from app.models.job_status import JobStatus
from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    company: str
    position: str
    status: JobStatus = JobStatus.APPLIED


class JobUpdate(BaseModel):
    company: str | None = None
    position: str | None = None
    status: JobStatus | None = None


class JobResponse(BaseModel):
    id: int
    company: str
    position: str
    status: JobStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )