"""
Job Intelligent - Job Scraper Service
Fetches real remote IT/Data jobs from Remotive API to populate the database.
"""
import httpx
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models.job import Job

logger = logging.getLogger(__name__)

# Remotive API URL Base
REMOTIVE_API_BASE = "https://remotive.com/api/remote-jobs?category="

# Selected IT/Data related categories to scrape
IT_CATEGORIES = ["software-dev", "data", "qa", "devops", "product"]

def scrape_and_store_jobs(db: Session, limit: int = 100):
    """Fetch jobs from multiple external API categories and store them."""
    # Clear old seeded jobs to see the new ones from internet
    db.query(Job).delete()
    db.commit()

    logger.info(f"Fetching up to {limit} real jobs across {len(IT_CATEGORIES)} IT domains...")
    
    added_count = 0
    
    try:
        with httpx.Client(timeout=20.0) as client:
            for category in IT_CATEGORIES:
                if added_count >= limit:
                    break
                    
                logger.info(f"Fetching category: {category}...")
                response = client.get(f"{REMOTIVE_API_BASE}{category}")
                response.raise_for_status()
                data = response.json()
                jobs_data = data.get("jobs", [])
                
                if not jobs_data:
                    logger.warning(f"No jobs found for category {category}.")
                    continue

                for job_data in jobs_data:
                    if added_count >= limit:
                        break
                        
                    # The API provides tags which we can use as skills
                    skills = job_data.get("tags", [])
                    title = job_data.get("title", "Unknown Role")
                    
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
        logger.info(f"✅ Successfully scraped and saved a total of {added_count} relevant jobs.")

    except httpx.RequestError as e:
        logger.error(f"❌ Failed to fetch jobs from API: {e}")
        db.rollback()
    except Exception as e:
        logger.error(f"❌ Error while saving scraped jobs: {e}")
        db.rollback()
