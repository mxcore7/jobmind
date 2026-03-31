"""
Job Intelligent - User Service
Business logic for user management.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.models.user import User
from backend.schemas.user import UserCreate, UserUpdate
from backend.core.security import hash_password, verify_password


def create_user(db: Session, user_data: UserCreate) -> User:
    """Register a new user. Raises 400 if email already exists."""
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un compte avec cet email existe déjà",
        )
    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
        skills=user_data.skills,
        experience=user_data.experience,
        preferences={},
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    """Authenticate user by email/password. Raises 401 on failure."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )
    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    """Get a user by ID. Raises 404 if not found."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé",
        )
    return user


def update_user(db: Session, user: User, updates: UserUpdate) -> User:
    """Update user profile fields."""
    if updates.full_name is not None:
        user.full_name = updates.full_name
    if updates.skills is not None:
        user.skills = updates.skills
    if updates.experience is not None:
        user.experience = updates.experience
    if updates.preferences is not None:
        user.preferences = updates.preferences
    db.commit()
    db.refresh(user)
    return user
