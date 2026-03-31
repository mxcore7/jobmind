"""
Job Intelligent - Favorites Routes
Endpoints for managing saved/favorite jobs.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.core.dependencies import get_db, get_current_user
from backend.models.user import User
from backend.schemas.job import JobOut
from backend.services.job_service import add_favorite, remove_favorite, get_favorites

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.get("", response_model=list[JobOut])
def list_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all favorite jobs for the current user."""
    return get_favorites(db, current_user.id)


@router.post("/{job_id}", status_code=201)
def add_to_favorites(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a job to favorites."""
    add_favorite(db, current_user.id, job_id)
    return {"message": "Job ajouté aux favoris"}


@router.delete("/{job_id}")
def remove_from_favorites(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove a job from favorites."""
    remove_favorite(db, current_user.id, job_id)
    return {"message": "Job retiré des favoris"}
