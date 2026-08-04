from sqlalchemy.orm import Session

from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate


class JobService:

    @staticmethod
    def create_job(db: Session, job: JobCreate):
        return JobRepository.create(db, job)