"""
Job Intelligent - User Schemas
Pydantic models for user-related request/response payloads.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    skills: list[str] = []
    experience: str | None = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    full_name: Optional[str] = None
    skills: Optional[list[str]] = None
    experience: Optional[str] = None
    preferences: Optional[dict] = None


class UserOut(BaseModel):
    """Schema for user response (no password)."""
    id: int
    email: str
    full_name: str
    skills: list[str]
    experience: str
    preferences: dict
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserOut
