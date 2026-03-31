"""
Job Intelligent - Search Service
Elasticsearch integration for advanced job search.
Falls back to PostgreSQL full-text search if Elasticsearch is unavailable.
"""
from typing import Optional
from elasticsearch import Elasticsearch, ConnectionError as ESConnectionError
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.models.job import Job

# Elasticsearch client (lazy init)
_es_client: Optional[Elasticsearch] = None
ES_INDEX = "jobs"


def _get_es() -> Optional[Elasticsearch]:
    """Get or create the Elasticsearch client. Returns None if unavailable."""
    global _es_client
    if _es_client is None:
        try:
            _es_client = Elasticsearch(settings.ELASTICSEARCH_URL)
            if not _es_client.ping():
                _es_client = None
        except Exception:
            _es_client = None
    return _es_client


def ensure_index():
    """Create the Elasticsearch jobs index if it doesn't exist."""
    es = _get_es()
    if es is None:
        return
    if not es.indices.exists(index=ES_INDEX):
        es.indices.create(
            index=ES_INDEX,
            body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text", "analyzer": "french"},
                        "description": {"type": "text", "analyzer": "french"},
                        "company": {"type": "keyword"},
                        "location": {"type": "keyword"},
                        "job_type": {"type": "keyword"},
                        "skills_required": {"type": "keyword"},
                        "source": {"type": "keyword"},
                    }
                }
            },
        )


def index_job(job: Job):
    """Index a job document in Elasticsearch."""
    es = _get_es()
    if es is None:
        return
    es.index(
        index=ES_INDEX,
        id=job.id,
        body={
            "title": job.title,
            "description": job.description,
            "company": job.company,
            "location": job.location,
            "job_type": job.job_type,
            "skills_required": job.skills_required or [],
            "source": job.source,
        },
    )


def search_jobs_es(
    query: Optional[str] = None,
    skills: Optional[list[str]] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
) -> list[int]:
    """Search jobs using Elasticsearch. Returns list of job IDs."""
    es = _get_es()
    if es is None:
        return []

    must_clauses = []
    filter_clauses = []

    if query:
        must_clauses.append({
            "multi_match": {
                "query": query,
                "fields": ["title^3", "description", "company"],
                "fuzziness": "AUTO",
            }
        })

    if skills:
        filter_clauses.append({"terms": {"skills_required": skills}})

    if location:
        filter_clauses.append({"term": {"location": location}})

    if job_type:
        filter_clauses.append({"term": {"job_type": job_type}})

    body = {
        "query": {
            "bool": {
                "must": must_clauses or [{"match_all": {}}],
                "filter": filter_clauses,
            }
        },
        "size": 50,
    }

    try:
        result = es.search(index=ES_INDEX, body=body)
        return [int(hit["_id"]) for hit in result["hits"]["hits"]]
    except Exception:
        return []


def search_jobs_fallback(
    db: Session,
    query: Optional[str] = None,
    skills: Optional[list[str]] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
) -> list[Job]:
    """Fallback search using PostgreSQL ILIKE when Elasticsearch is unavailable."""
    q = db.query(Job)
    if query:
        q = q.filter(
            Job.title.ilike(f"%{query}%") | Job.description.ilike(f"%{query}%")
        )
    if location:
        q = q.filter(Job.location.ilike(f"%{location}%"))
    if job_type:
        q = q.filter(Job.job_type == job_type)
    if skills:
        # Match jobs that have at least one of the requested skills
        from sqlalchemy import or_
        skill_filters = [Job.skills_required.any(skill) for skill in skills]
        q = q.filter(or_(*skill_filters))
    return q.order_by(Job.created_at.desc()).limit(50).all()
