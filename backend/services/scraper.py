"""
Job Intelligent - Job Scraper Service
Fetches real remote Data jobs from Remotive API to populate the database.
"""
import httpx
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models.job import Job

logger = logging.getLogger(__name__)

# Remotive API for real Data/Software jobs
REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs?category=software-dev"

def scrape_and_store_jobs(db: Session, limit: int = 50):
    """Fetch jobs from external API and store them in the database."""
    # Clear old seeded jobs to see the new ones from internet
    db.query(Job).delete()
    db.commit()

    logger.info("Fetching real data jobs from Remotive API...")
    try:
        response = httpx.get(REMOTIVE_API_URL, timeout=15.0)
        response.raise_for_status()
        data = response.json()
        jobs_data = data.get("jobs", [])
        
        if not jobs_data:
            logger.warning("No jobs found from API.")
            return

        added_count = 0
        for job_data in jobs_data[:limit]:
            # The API provides tags which we can use as skills
            skills = job_data.get("tags", [])
            title = job_data.get("title", "Data Role")
            
            # Simple parsing for job_type based on the job data
            job_type = job_data.get("job_type", "").replace("_", " ").title()
            if not job_type:
                job_type = "Full Time"

            # Create new job entity
            new_job = Job(
                title=title,
                description=job_data.get("description", ""),  # Contains HTML
                company=job_data.get("company_name", "Unknown"),
                location=job_data.get("candidate_required_location", "Remote"),
                job_type=job_type,
                skills_required=skills,
                source="Remotive",
                created_at=datetime.utcnow()
            )
            db.add(new_job)
            added_count += 1
        
        db.commit()
        logger.info(f"✅ Successfully scraped and saved {added_count} jobs.")

    except httpx.RequestError as e:
        logger.error(f"❌ Failed to fetch jobs from API: {e}")
    except Exception as e:
        logger.error(f"❌ Error while saving scraped jobs: {e}")
        db.rollback()
