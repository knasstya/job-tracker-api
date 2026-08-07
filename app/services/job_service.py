
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate, JobUpdate


class JobService:

    @staticmethod
    def create_job(db: Session, job: JobCreate):
        return JobRepository.create(db, job)

    @staticmethod
    def get_jobs(
        db: Session,
        status: str | None = None,
        limit: int = 10,
        offset: int = 0
    ):
        return JobRepository.get_all(
            db,
            status,
            limit,
            offset
        )

    @staticmethod
    def get_job(db: Session, job_id: int):
        job = JobRepository.get_by_id(db, job_id)

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        return job
    
    @staticmethod
    def update_job(db: Session, job_id: int, job_data: JobUpdate):
        job = JobRepository.get_by_id(db, job_id)

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        return JobRepository.update(db, job, job_data)

    @staticmethod
    def delete_job(db: Session, job_id: int):
        job = JobRepository.get_by_id(db, job_id)

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        JobRepository.delete(db, job)