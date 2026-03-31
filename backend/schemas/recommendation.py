"""
Job Intelligent - Recommendation Schemas
Pydantic models for recommendation responses.
"""
from pydantic import BaseModel
from backend.schemas.job import JobOut


class RecommendationOut(BaseModel):
    """A recommended job with a relevance score."""
    job: JobOut
    score: float
    match_type: str  # "keyword" or "semantic"
