# Job Intelligent 🧠

Plateforme intelligente de recherche d'emploi dans le domaine de la Data.

## 🏗️ Architecture

```
jobmind/
├── backend/                    # API FastAPI (Python)
│   ├── main.py                 # Point d'entrée
│   ├── core/                   # Config, sécurité, dépendances
│   ├── models/                 # Modèles SQLAlchemy
│   ├── schemas/                # Schémas Pydantic
│   ├── routes/                 # Endpoints API REST
│   ├── services/               # Logique métier
│   ├── recommender/            # Moteur de recommandation IA
│   ├── database/               # Session DB + init
│   └── tests/                  # Tests unitaires
├── lib/                        # Application Flutter (Web + Mobile)
│   ├── core/                   # Thème, routeur, constantes
│   ├── data/                   # Couche données (API, modèles, repos)
│   ├── domain/                 # Couche domaine (entités, interfaces)
│   └── presentation/           # Couche présentation (providers, pages, widgets)
├── docker-compose.yml          # PostgreSQL + Elasticsearch + API
└── assets/                     # Icônes, images, polices
```

## 🚀 Démarrage rapide

### 1. Infrastructure (Docker)

```bash
# Lancer PostgreSQL + Elasticsearch
docker-compose up -d postgres elasticsearch
```

### 2. Backend Python

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Copier la config
copy .env.example .env         # Windows
# cp .env.example .env         # Linux/Mac

# Lancer l'API
uvicorn backend.main:app --reload
```

L'API est accessible sur **http://localhost:8000**
Documentation Swagger : **http://localhost:8000/docs**

### 3. Frontend Flutter

```bash
# Installer les dépendances Flutter
flutter pub get

# Lancer sur Chrome (Web)
flutter run -d chrome

# Lancer sur Android
flutter run -d android

# Lancer sur iOS
flutter run -d ios
```

## 🔗 Endpoints API

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/auth/register` | Inscription |
| `POST` | `/auth/login` | Connexion |
| `GET` | `/jobs` | Liste des offres |
| `GET` | `/jobs/{id}` | Détail d'une offre |
| `POST` | `/jobs` | Créer une offre |
| `GET` | `/recommendations/{user_id}` | Recommandations personnalisées |
| `GET` | `/search` | Recherche avancée |
| `GET` | `/favorites` | Mes favoris |
| `POST` | `/favorites/{job_id}` | Ajouter aux favoris |
| `DELETE` | `/favorites/{job_id}` | Retirer des favoris |
| `GET` | `/history` | Historique de consultation |
| `GET` | `/profile` | Mon profil |
| `PUT` | `/profile` | Modifier mon profil |

## 🧠 Système de recommandation

**Niveau 1** — Matching par mots-clés (similarité de Jaccard sur les compétences)
**Niveau 2** — Similarité sémantique via `sentence-transformers` (modèle `all-MiniLM-L6-v2`)

Score combiné : `40% keyword + 60% semantic`

## 🛠️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Python, FastAPI, SQLAlchemy |
| Base de données | PostgreSQL 16 |
| Recherche | Elasticsearch 8.15 |
| IA / NLP | sentence-transformers |
| Frontend | Flutter (Web + Android + iOS) |
| État | Riverpod |
| Routing | GoRouter |
| HTTP | Dio |
| Auth | JWT (python-jose + passlib/bcrypt) |

## 🧪 Tests

```bash
# Tests backend
cd backend
python -m pytest tests/ -v

# Analyse Flutter
flutter analyze
```

## 🐳 Docker complet

```bash
# Tout lancer (API + Postgres + Elasticsearch)
docker-compose up -d

# Voir les logs
docker-compose logs -f api
```

## 📱 Screenshots

L'application comprend :
- **Splash Screen** animé avec gradient
- **Login / Register** avec ajout de compétences
- **Home** avec onglets Offres + Recommandations
- **Détail Job** avec barre d'application en gradient
- **Recherche** avec filtres avancés
- **Favoris** avec gestion en temps réel
- **Profil** avec édition des compétences

## 📝 Licence

Projet privé — Tous droits réservés.
