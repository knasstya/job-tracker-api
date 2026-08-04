from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.core.database import SessionLocal
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import JobService


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    return JobService.create_job(db, job)

@router.get("/", response_model=list[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    return JobService.get_jobs(db)