
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate, JobUpdate
from app.models.job_sort import JobSortField, SortOrder
from app.models.job_status import JobStatus

class JobService:

    @staticmethod
    def create_job(
        db: Session,
        job: JobCreate,
        user_id: int
    ):
        return JobRepository.create(
            db,
            job,
            user_id
        )

    @staticmethod
    def get_jobs(
        db: Session,
        user_id: int,
        status: JobStatus | None = None,
        search: str | None = None,
        limit: int = 10,
        offset: int = 0,
        sort_by: JobSortField = JobSortField.CREATED_AT,
        order: SortOrder = SortOrder.DESC
    ):
        return JobRepository.get_all(
            db,
            user_id,
            status,
            search,
            limit,
            offset,
            sort_by,
            order
        )

    @staticmethod
    def get_job(
        db: Session,
        job_id: int,
        user_id: int
    ):
        job = JobRepository.get_by_id(
            db,
            job_id,
            user_id
        )

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        return job
    
    @staticmethod
    def update_job(
        db: Session,
        job_id: int,
        job_data: JobUpdate,
        user_id: int
    ):
        job = JobRepository.get_by_id(
            db,
            job_id,
            user_id
        )

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        return JobRepository.update(
            db,
            job,
            job_data
        )

    @staticmethod
    def delete_job(
        db: Session,
        job_id: int,
        user_id: int
    ):
        job = JobRepository.get_by_id(
            db,
            job_id,
            user_id
        )

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        JobRepository.delete(db, job)