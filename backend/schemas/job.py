"""
Job Intelligent - Job Schemas
Pydantic models for job-related request/response payloads.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobCreate(BaseModel):
    """Schema for creating a new job."""
    title: str
    description: str
    company: str
    location: str
    job_type: str = "CDI"
    skills_required: list[str] = []
    source: str = "internal"


class JobUpdate(BaseModel):
    """Schema for updating a job."""
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    skills_required: Optional[list[str]] = None


class JobOut(BaseModel):
    """Schema for job response."""
    id: int
    title: str
    description: str
    company: str
    location: str
    job_type: str
    skills_required: list[str]
    source: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
