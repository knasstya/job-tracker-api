from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, Query

from app.core.database import get_db
from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.services.job_service import JobService

from app.core.auth import get_current_user
from app.models.user import User

from app.models.job_sort import JobSortField, SortOrder
from app.models.job_status import JobStatus

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/", response_model=JobResponse, status_code=201)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return JobService.create_job(
        db,
        job,
        current_user.id
    )

@router.get("/", response_model=list[JobResponse])
def get_jobs(
    status: JobStatus | None = None,
    search: str | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: JobSortField = JobSortField.CREATED_AT,
    order: SortOrder = SortOrder.DESC,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return JobService.get_jobs(
        db,
        current_user.id,
        status,
        search,
        limit,
        offset,
        sort_by,
        order
    )

@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return JobService.get_job(
        db,
        job_id,
        current_user.id
    )

@router.patch("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return JobService.update_job(
        db,
        job_id,
        job_data,
        current_user.id
    )

@router.delete("/{job_id}", status_code=204)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    JobService.delete_job(
        db,
        job_id,
        current_user.id
    )

    return Response(status_code=204)