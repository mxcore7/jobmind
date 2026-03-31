"""
Job Intelligent - Recommendation Engine
Two-level recommendation system:
  Level 1: Keyword matching (Jaccard similarity on skills)
  Level 2: Semantic similarity using sentence-transformers embeddings
"""
import logging
from typing import Optional

from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.job import Job
from backend.schemas.job import JobOut
from backend.schemas.recommendation import RecommendationOut

logger = logging.getLogger(__name__)

# Lazy-loaded sentence transformer model
_model = None


def _get_model():
    """Lazy-load the sentence-transformers model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            from backend.core.config import settings
            _model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info("✅ Sentence-transformers model loaded successfully.")
        except Exception as e:
            logger.warning(f"⚠️ Could not load sentence-transformers: {e}. Using keyword-only mode.")
            _model = False  # Sentinel: don't retry
    return _model if _model is not False else None


def _jaccard_similarity(set_a: set, set_b: set) -> float:
    """Compute Jaccard similarity between two sets."""
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def _cosine_similarity(vec_a, vec_b) -> float:
    """Compute cosine similarity between two vectors."""
    import numpy as np
    dot = float(np.dot(vec_a, vec_b))
    norm_a = float(np.linalg.norm(vec_a))
    norm_b = float(np.linalg.norm(vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def get_recommendations(
    db: Session,
    user: User,
    limit: int = 20,
    use_semantic: bool = True,
) -> list[RecommendationOut]:
    """
    Generate job recommendations for a user.
    Combines keyword matching and (optionally) semantic similarity.
    """
    user_skills = set(s.lower() for s in (user.skills or []))
    if not user_skills:
        # No skills = return latest jobs with zero score
        jobs = db.query(Job).order_by(Job.created_at.desc()).limit(limit).all()
        return [
            RecommendationOut(
                job=JobOut.model_validate(j),
                score=0.0,
                match_type="none",
            )
            for j in jobs
        ]

    all_jobs = db.query(Job).all()
    scored_jobs: list[tuple[Job, float, str]] = []

    # --- Level 1: Keyword matching ---
    for job in all_jobs:
        job_skills = set(s.lower() for s in (job.skills_required or []))
        keyword_score = _jaccard_similarity(user_skills, job_skills)
        scored_jobs.append((job, keyword_score, "keyword"))

    # --- Level 2: Semantic similarity (optional) ---
    model = _get_model() if use_semantic else None
    if model is not None:
        try:
            user_text = f"{user.full_name} {user.experience} {' '.join(user.skills or [])}"
            user_embedding = model.encode(user_text)

            for i, (job, keyword_score, _) in enumerate(scored_jobs):
                job_text = f"{job.title} {job.description} {' '.join(job.skills_required or [])}"
                job_embedding = model.encode(job_text)
                semantic_score = _cosine_similarity(user_embedding, job_embedding)

                # Combined score: 40% keyword + 60% semantic
                combined = 0.4 * keyword_score + 0.6 * semantic_score
                scored_jobs[i] = (job, combined, "semantic")
        except Exception as e:
            logger.warning(f"Semantic scoring failed: {e}")

    # Sort by score descending
    scored_jobs.sort(key=lambda x: x[1], reverse=True)

    return [
        RecommendationOut(
            job=JobOut.model_validate(j),
            score=round(score, 4),
            match_type=match_type,
        )
        for j, score, match_type in scored_jobs[:limit]
    ]
