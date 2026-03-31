"""
Job Intelligent - FastAPI Application Entry Point
Main application with CORS, router mounting, and startup lifecycle.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.database.init_db import init_db
from backend.database.session import SessionLocal
from backend.services.scraper import scrape_and_store_jobs
from backend.routes import auth, jobs, recommendations, search, favorites, history, profile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    logger.info("🚀 Starting Job Intelligent API...")
    # Initialize database tables
    init_db()
    logger.info("✅ Database tables created.")

    # Scrape real jobs
    db = SessionLocal()
    try:
        scrape_and_store_jobs(db, limit=40)
    finally:
        db.close()

    # Try to initialize Elasticsearch index
    try:
        from backend.services.search_service import ensure_index
        ensure_index()
        logger.info("✅ Elasticsearch index ready.")
    except Exception as e:
        logger.warning(f"⚠️ Elasticsearch unavailable: {e}. Using PostgreSQL fallback.")

    yield
    logger.info("👋 Shutting down Job Intelligent API.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Plateforme intelligente de recherche d'emploi dans le domaine de la Data",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(recommendations.router)
app.include_router(search.router)
app.include_router(favorites.router)
app.include_router(history.router)
app.include_router(profile.router)


@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
