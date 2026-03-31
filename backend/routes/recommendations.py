"""
Job Intelligent - Recommendation Routes
Endpoint for personalized job recommendations.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.core.dependencies import get_db, get_current_user
from backend.models.user import User
from backend.schemas.recommendation import RecommendationOut
from backend.services.user_service import get_user_by_id
from backend.recommender.engine import get_recommendations

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/{user_id}", response_model=list[RecommendationOut])
def recommend_jobs(
    user_id: int,
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get personalized job recommendations for a user."""
    target_user = get_user_by_id(db, user_id)
    return get_recommendations(db, target_user, limit=limit)
