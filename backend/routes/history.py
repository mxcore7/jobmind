"""
Job Intelligent - History Routes
Endpoints for job consultation history.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.core.dependencies import get_db, get_current_user
from backend.models.user import User
from backend.schemas.job import JobOut
from backend.services.job_service import get_history

router = APIRouter(prefix="/history", tags=["History"])


@router.get("", response_model=list[JobOut])
def list_history(
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the current user's job viewing history."""
    return get_history(db, current_user.id, limit=limit)
