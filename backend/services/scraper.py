"""
Job Intelligent - Job Scraper Service
Fetches real remote jobs from Remotive API across multiple categories.
"""
import httpx
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models.job import Job

logger = logging.getLogger(__name__)

# Base URL for the Remotive API
REMOTIVE_API_BASE = "https://remotive.com/api/remote-jobs"

# All available Remotive categories to maximize job coverage
REMOTIVE_CATEGORIES = [
    "software-dev",
    "data",
    "devops-sysadmin",
    "product",
    "design",
    "qa",
    "marketing",
    "finance-legal",
    "customer-support",
    "writing",
    "human-resources",
    "sales",
    "business",
    "all-others",
]


def scrape_and_store_jobs(db: Session, limit_per_category: int = 30, total_limit: int = 300):
    """Fetch jobs from Remotive API across all categories and store them.

    Args:
        db: database session
        limit_per_category: max jobs to keep per category
        total_limit: global cap on total jobs stored
    """
    # Clear old jobs to refresh with latest data
    db.query(Job).delete()
    db.commit()

    logger.info(f"🔍 Fetching jobs from {len(REMOTIVE_CATEGORIES)} Remotive categories...")
    added_count = 0
    seen_titles: set[str] = set()  # avoid duplicates across categories

    for category in REMOTIVE_CATEGORIES:
        if added_count >= total_limit:
            break

        url = f"{REMOTIVE_API_BASE}?category={category}"
        try:
            response = httpx.get(url, timeout=15.0)
            response.raise_for_status()
            jobs_data = response.json().get("jobs", [])

            if not jobs_data:
                logger.info(f"  ⚠️  No jobs in category '{category}'")
                continue

            cat_count = 0
            for job_data in jobs_data:
                if added_count >= total_limit or cat_count >= limit_per_category:
                    break

                title = job_data.get("title", "Remote Role")
                company = job_data.get("company_name", "Unknown")
                dedup_key = f"{title}|{company}"
                if dedup_key in seen_titles:
                    continue
                seen_titles.add(dedup_key)

                skills = job_data.get("tags", [])
                job_type = job_data.get("job_type", "").replace("_", " ").title() or "Full Time"

                new_job = Job(
                    title=title,
                    description=job_data.get("description", ""),
                    company=company,
                    location=job_data.get("candidate_required_location", "Remote"),
                    job_type=job_type,
                    skills_required=skills,
                    source="Remotive",
                    created_at=datetime.utcnow(),
                )
                db.add(new_job)
                added_count += 1
                cat_count += 1

            logger.info(f"  ✅ {category}: +{cat_count} jobs")

        except httpx.RequestError as e:
            logger.warning(f"  ❌ Failed to fetch '{category}': {e}")
            continue
        except Exception as e:
            logger.error(f"  ❌ Error processing '{category}': {e}")
            continue

    try:
        db.commit()
        logger.info(f"🎉 Total: {added_count} unique jobs saved across {len(REMOTIVE_CATEGORIES)} categories.")
    except Exception as e:
        logger.error(f"❌ Database commit failed: {e}")
        db.rollback()
