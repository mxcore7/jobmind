"""
Job Intelligent - Job Model
SQLAlchemy model for the jobs table.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func

from backend.database.session import Base


class Job(Base):
    """Job posting model."""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False, index=True)
    job_type = Column(String(50), default="CDI")  # CDI, CDD, Stage, Freelance
    skills_required = Column(ARRAY(String), default=[])
    source = Column(String(100), default="internal")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
