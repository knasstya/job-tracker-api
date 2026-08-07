from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response

from app.core.database import get_db
from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.services.job_service import JobService


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    return JobService.create_job(db, job)

@router.get("/", response_model=list[JobResponse])
def get_jobs(
    status: str | None = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return JobService.get_jobs(
        db,
        status,
        limit,
        offset
    )

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    return JobService.get_job(db, job_id)

@router.patch("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db)
):
    return JobService.update_job(db, job_id, job_data)

@router.delete("/{job_id}", status_code=204)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    JobService.delete_job(db, job_id)
    return Response(status_code=204)