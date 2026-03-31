"""
Job Intelligent - Database Initialization
Create all tables and optionally seed demo data.
"""
from backend.database.session import engine, Base

# Import all models so Base.metadata knows about them
from backend.models.user import User  # noqa: F401
from backend.models.job import Job  # noqa: F401
from backend.models.favorite import Favorite  # noqa: F401
from backend.models.history import History  # noqa: F401


def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def seed_demo_jobs(db):
    """Insert demo job postings for testing."""
    from backend.models.job import Job

    demo_jobs = [
        Job(
            title="Data Scientist Senior",
            description="Nous recherchons un Data Scientist expérimenté pour rejoindre notre équipe IA. "
                        "Vous travaillerez sur des modèles de machine learning, l'analyse prédictive "
                        "et le traitement du langage naturel.",
            company="DataCorp",
            location="Paris",
            job_type="CDI",
            skills_required=["Python", "Machine Learning", "TensorFlow", "SQL", "NLP"],
            source="internal",
        ),
        Job(
            title="Data Engineer",
            description="Rejoignez notre équipe data pour concevoir et maintenir des pipelines de données "
                        "à grande échelle. Expérience avec les outils Big Data requise.",
            company="TechFlow",
            location="Lyon",
            job_type="CDI",
            skills_required=["Python", "Apache Spark", "Airflow", "SQL", "AWS"],
            source="internal",
        ),
        Job(
            title="Data Analyst",
            description="Analyser les données métier pour fournir des insights actionnables. "
                        "Créer des tableaux de bord et des rapports pour les parties prenantes.",
            company="InsightLab",
            location="Marseille",
            job_type="CDI",
            skills_required=["SQL", "Python", "Power BI", "Excel", "Statistiques"],
            source="internal",
        ),
        Job(
            title="ML Engineer",
            description="Déployer et optimiser des modèles de machine learning en production. "
                        "Travailler avec les équipes DevOps pour le CI/CD des modèles.",
            company="AI Solutions",
            location="Paris",
            job_type="CDI",
            skills_required=["Python", "Docker", "Kubernetes", "MLflow", "PyTorch"],
            source="internal",
        ),
        Job(
            title="Business Intelligence Analyst",
            description="Concevoir des solutions BI pour aider à la prise de décision. "
                        "Expertise Power BI et data warehousing requise.",
            company="DecisionTech",
            location="Bordeaux",
            job_type="CDD",
            skills_required=["Power BI", "SQL", "DAX", "Data Warehouse", "ETL"],
            source="internal",
        ),
        Job(
            title="Data Architect",
            description="Définir l'architecture data de l'entreprise et superviser la gouvernance "
                        "des données. Expérience cloud requise.",
            company="CloudData",
            location="Toulouse",
            job_type="CDI",
            skills_required=["AWS", "Azure", "Snowflake", "SQL", "Data Modeling"],
            source="internal",
        ),
        Job(
            title="NLP Engineer",
            description="Développer des solutions de traitement du langage naturel pour l'analyse "
                        "de texte et les chatbots intelligents.",
            company="LinguaTech",
            location="Paris",
            job_type="CDI",
            skills_required=["Python", "NLP", "Transformers", "spaCy", "Deep Learning"],
            source="internal",
        ),
        Job(
            title="Data Scientist Junior",
            description="Poste junior en data science. Formation et encadrement assurés. "
                        "Première expérience en analyse de données souhaitée.",
            company="StartupData",
            location="Nantes",
            job_type="Stage",
            skills_required=["Python", "Pandas", "Scikit-learn", "SQL", "Statistiques"],
            source="internal",
        ),
    ]

    # Only seed if no jobs exist
    if db.query(Job).count() == 0:
        db.add_all(demo_jobs)
        db.commit()
        print(f"✅ {len(demo_jobs)} offres d'emploi de démonstration ajoutées.")
    else:
        print("ℹ️  Des offres existent déjà, seed ignoré.")
