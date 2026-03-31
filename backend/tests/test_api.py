"""
Job Intelligent - Backend Tests
Test suite for auth, jobs, and recommendations.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database.session import Base
from backend.core.dependencies import get_db
from backend.main import app

# In-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Create tables before each test and drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ==================== Auth Tests ====================

class TestAuth:
    """Tests for authentication endpoints."""

    def test_register_success(self):
        response = client.post("/auth/register", json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User",
            "skills": ["Python", "SQL"],
        })
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["full_name"] == "Test User"

    def test_register_duplicate_email(self):
        # First registration
        client.post("/auth/register", json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User",
        })
        # Duplicate
        response = client.post("/auth/register", json={
            "email": "test@example.com",
            "password": "password456",
            "full_name": "Test User 2",
        })
        assert response.status_code == 400

    def test_login_success(self):
        # Register first
        client.post("/auth/register", json={
            "email": "login@example.com",
            "password": "password123",
            "full_name": "Login User",
        })
        # Login
        response = client.post("/auth/login", json={
            "email": "login@example.com",
            "password": "password123",
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self):
        # Register first
        client.post("/auth/register", json={
            "email": "login@example.com",
            "password": "password123",
            "full_name": "Login User",
        })
        # Wrong password
        response = client.post("/auth/login", json={
            "email": "login@example.com",
            "password": "wrong_password",
        })
        assert response.status_code == 401


# ==================== Jobs Tests ====================

class TestJobs:
    """Tests for job endpoints."""

    def _get_token(self) -> str:
        """Helper: register and get a token."""
        resp = client.post("/auth/register", json={
            "email": "jobuser@example.com",
            "password": "password123",
            "full_name": "Job User",
            "skills": ["Python"],
        })
        return resp.json()["access_token"]

    def test_list_jobs_empty(self):
        response = client.get("/jobs")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_and_list_jobs(self):
        token = self._get_token()
        headers = {"Authorization": f"Bearer {token}"}

        # Create a job
        resp = client.post("/jobs", json={
            "title": "Data Scientist",
            "description": "Analyse des données",
            "company": "TestCorp",
            "location": "Paris",
            "skills_required": ["Python", "ML"],
        }, headers=headers)
        assert resp.status_code == 201
        assert resp.json()["title"] == "Data Scientist"

        # List jobs
        resp = client.get("/jobs")
        assert len(resp.json()) == 1

    def test_get_job_by_id(self):
        token = self._get_token()
        headers = {"Authorization": f"Bearer {token}"}

        # Create job
        create_resp = client.post("/jobs", json={
            "title": "Data Engineer",
            "description": "Pipeline de données",
            "company": "DataCo",
            "location": "Lyon",
        }, headers=headers)
        job_id = create_resp.json()["id"]

        # Get job
        resp = client.get(f"/jobs/{job_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["title"] == "Data Engineer"


# ==================== Recommendations Tests ====================

class TestRecommendations:
    """Tests for the recommendation engine."""

    def test_recommendations_with_skills(self):
        # Register user with skills
        reg_resp = client.post("/auth/register", json={
            "email": "reco@example.com",
            "password": "password123",
            "full_name": "Reco User",
            "skills": ["Python", "Machine Learning", "SQL"],
        })
        token = reg_resp.json()["access_token"]
        user_id = reg_resp.json()["user"]["id"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create jobs
        client.post("/jobs", json={
            "title": "Data Scientist",
            "description": "ML and Python",
            "company": "A",
            "location": "Paris",
            "skills_required": ["Python", "Machine Learning", "TensorFlow"],
        }, headers=headers)

        client.post("/jobs", json={
            "title": "Frontend Developer",
            "description": "React and CSS",
            "company": "B",
            "location": "Paris",
            "skills_required": ["React", "CSS", "JavaScript"],
        }, headers=headers)

        # Get recommendations
        resp = client.get(f"/recommendations/{user_id}", headers=headers)
        assert resp.status_code == 200
        recs = resp.json()
        assert len(recs) == 2
        # Data Scientist should rank higher (matching skills)
        assert recs[0]["job"]["title"] == "Data Scientist"
        assert recs[0]["score"] > recs[1]["score"]


# ==================== Health Check ====================

class TestHealth:
    """Test health check endpoint."""

    def test_health(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
