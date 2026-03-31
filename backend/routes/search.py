"""
Job Intelligent - Search Routes
Advanced search powered by Elasticsearch with PostgreSQL fallback.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from backend.core.dependencies import get_db
from backend.schemas.job import JobOut
from backend.services.search_service import search_jobs_es, search_jobs_fallback
from backend.models.job import Job

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("", response_model=list[JobOut])
def search_jobs(
    q: Optional[str] = Query(None, description="Texte de recherche libre"),
    skills: Optional[str] = Query(None, description="Compétences (séparées par des virgules)"),
    location: Optional[str] = Query(None, description="Localisation"),
    job_type: Optional[str] = Query(None, description="Type de contrat (CDI, CDD, Stage, Freelance)"),
    db: Session = Depends(get_db),
):
    """
    Search jobs with optional filters.
    Uses Elasticsearch when available, falls back to PostgreSQL.
    """
    skills_list = [s.strip() for s in skills.split(",")] if skills else None

    # Try Elasticsearch first
    es_ids = search_jobs_es(query=q, skills=skills_list, location=location, job_type=job_type)

    if es_ids:
        # Fetch full job objects from DB using ES result IDs
        jobs = db.query(Job).filter(Job.id.in_(es_ids)).all()
        # Preserve ES ordering
        id_order = {jid: idx for idx, jid in enumerate(es_ids)}
        jobs.sort(key=lambda j: id_order.get(j.id, 999))
        return jobs

    # Fallback to PostgreSQL search
    return search_jobs_fallback(db, query=q, skills=skills_list, location=location, job_type=job_type)
