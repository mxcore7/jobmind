"""
Job Intelligent - Job Service
Business logic for job management.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional

from backend.models.job import Job
from backend.models.favorite import Favorite
from backend.models.history import History
from backend.schemas.job import JobCreate, JobUpdate


def get_all_jobs(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
) -> list[Job]:
    """Get all jobs with optional filters and pagination."""
    query = db.query(Job)
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if job_type:
        query = query.filter(Job.job_type == job_type)
    return query.order_by(Job.created_at.desc()).offset(skip).limit(limit).all()


def get_job_by_id(db: Session, job_id: int) -> Job:
    """Get a single job by ID. Raises 404 if not found."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre d'emploi non trouvée",
        )
    return job


def create_job(db: Session, job_data: JobCreate) -> Job:
    """Create a new job posting."""
    job = Job(**job_data.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def update_job(db: Session, job_id: int, job_data: JobUpdate) -> Job:
    """Update an existing job posting."""
    job = get_job_by_id(db, job_id)
    for field, value in job_data.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job


def delete_job(db: Session, job_id: int) -> None:
    """Delete a job posting."""
    job = get_job_by_id(db, job_id)
    db.delete(job)
    db.commit()


# --- Favorites ---

def add_favorite(db: Session, user_id: int, job_id: int) -> Favorite:
    """Add a job to user's favorites."""
    # Verify job exists
    get_job_by_id(db, job_id)
    existing = db.query(Favorite).filter(
        Favorite.user_id == user_id, Favorite.job_id == job_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce job est déjà dans vos favoris",
        )
    fav = Favorite(user_id=user_id, job_id=job_id)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav


def remove_favorite(db: Session, user_id: int, job_id: int) -> None:
    """Remove a job from user's favorites."""
    fav = db.query(Favorite).filter(
        Favorite.user_id == user_id, Favorite.job_id == job_id
    ).first()
    if not fav:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favori non trouvé",
        )
    db.delete(fav)
    db.commit()


def get_favorites(db: Session, user_id: int) -> list[Job]:
    """Get all favorite jobs for a user."""
    fav_ids = db.query(Favorite.job_id).filter(Favorite.user_id == user_id).all()
    job_ids = [fid[0] for fid in fav_ids]
    if not job_ids:
        return []
    return db.query(Job).filter(Job.id.in_(job_ids)).all()


# --- History ---

def record_view(db: Session, user_id: int, job_id: int) -> None:
    """Record that a user viewed a job."""
    entry = History(user_id=user_id, job_id=job_id)
    db.add(entry)
    db.commit()


def get_history(db: Session, user_id: int, limit: int = 50) -> list[Job]:
    """Get the user's job viewing history."""
    history_entries = (
        db.query(History)
        .filter(History.user_id == user_id)
        .order_by(History.viewed_at.desc())
        .limit(limit)
        .all()
    )
    job_ids = [h.job_id for h in history_entries]
    if not job_ids:
        return []
    return db.query(Job).filter(Job.id.in_(job_ids)).all()
