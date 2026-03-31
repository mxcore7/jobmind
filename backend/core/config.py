"""
Job Intelligent - Backend Configuration
Settings loaded from environment variables via Pydantic BaseSettings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Job Intelligent API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://jobintel:jobintel@localhost:5432/jobintel_db"

    # JWT
    JWT_SECRET_KEY: str = "super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440  # 24 hours

    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"

    # CORS
    CORS_ORIGINS: list[str] = ["*"]

    # Recommender
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
