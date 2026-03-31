"""
Job Intelligent - Auth Routes
Registration and login endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.core.dependencies import get_db
from backend.core.security import create_access_token
from backend.schemas.user import UserCreate, UserLogin, Token, UserOut
from backend.services.user_service import create_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and return a JWT token."""
    user = create_user(db, user_data)
    token = create_access_token(data={"sub": user.id})
    return Token(
        access_token=token,
        user=UserOut.model_validate(user),
    )


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate and return a JWT token."""
    user = authenticate_user(db, credentials.email, credentials.password)
    token = create_access_token(data={"sub": user.id})
    return Token(
        access_token=token,
        user=UserOut.model_validate(user),
    )
