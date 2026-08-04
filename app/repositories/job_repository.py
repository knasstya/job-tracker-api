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