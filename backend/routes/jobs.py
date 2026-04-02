"""
Job Intelligent - Job Routes
CRUD endpoints for job postings.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from backend.core.dependencies import get_db, get_current_user, get_optional_current_user
from backend.models.user import User
from backend.schemas.job import JobCreate, JobOut
from backend.services.job_service import (
    get_all_jobs,
    get_job_by_id,
    create_job,
    record_view,
)

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("", response_model=list[JobOut])
def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List all jobs with optional filters and pagination."""
    return get_all_jobs(db, skip=skip, limit=limit, location=location, job_type=job_type)


@router.get("/{job_id}", response_model=JobOut)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Get a single job by ID. Records view in history if user is authenticated."""
    job = get_job_by_id(db, job_id)
    if current_user:
        record_view(db, current_user.id, job.id)
    return job


@router.post("", response_model=JobOut, status_code=201)
def add_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new job posting (authenticated)."""
    return create_job(db, job_data)
