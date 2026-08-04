from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.job import JobCreate


class JobRepository:

    @staticmethod
    def create(db: Session, job: JobCreate) -> Job:
        db_job = Job(
            company=job.company,
            position=job.position
        )

        db.add(db_job)
        db.commit()
        db.refresh(db_job)

        return db_job

    @staticmethod
    def get_all(db: Session) -> list[Job]:
        return db.query(Job).all()

    @staticmethod
    def get_by_id(db: Session, job_id: int) -> Job | None:
        return db.query(Job).filter(Job.id == job_id).first()