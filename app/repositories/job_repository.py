from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate
from app.models.job_sort import JobSortField, SortOrder

class JobRepository:

    @staticmethod
    def create(
        db: Session,
        job: JobCreate,
        user_id: int
    ) -> Job:
        db_job = Job(
            company=job.company,
            position=job.position,
            status=job.status,
            user_id=user_id
        )

        db.add(db_job)
        db.commit()
        db.refresh(db_job)

        return db_job

    @staticmethod
    def get_all(
        db: Session,
        user_id: int,
        status: str | None = None,
        search: str | None = None,
        limit: int = 10,
        offset: int = 0,
        sort_by: JobSortField = JobSortField.CREATED_AT,
        order: SortOrder = SortOrder.DESC
    ) -> list[Job]:
        query = db.query(Job).filter(
            Job.user_id == user_id
        )

        if status:
            query = query.filter(
                Job.status == status
            )

        if search:
            query = query.filter(
                (Job.company.ilike(f"%{search}%")) |
                (Job.position.ilike(f"%{search}%"))
            )

        sort_column = {
            JobSortField.CREATED_AT: Job.created_at,
            JobSortField.COMPANY: Job.company,
            JobSortField.POSITION: Job.position
        }[sort_by]

        if order == SortOrder.ASC:
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        return (
            query
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        job_id: int,
        user_id: int
    ) -> Job | None:
        return (
            db.query(Job)
            .filter(
                Job.id == job_id,
                Job.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def update(db: Session, db_job: Job, job_data: JobUpdate) -> Job:
        if job_data.company is not None:
            db_job.company = job_data.company

        if job_data.position is not None:
            db_job.position = job_data.position

        if job_data.status is not None:
            db_job.status = job_data.status

        db.commit()
        db.refresh(db_job)

        return db_job

    @staticmethod
    def delete(db: Session, db_job: Job):
        db.delete(db_job)
        db.commit()