from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os

# Récupération des paramètres depuis les variables d'environnement
POSTGRES_DB = os.getenv("POSTGRES_DB", "appointments")
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pass")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")

print(f"Connecting to database {POSTGRES_DB} at {POSTGRES_HOST}:{POSTGRES_PORT} as user {POSTGRES_USER}")
DATABASE_URL = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Création d'une session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Déclaration de la base de modèles
Base = declarative_base()

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Fournit une session de base de données pour les opérations CRUD.
    Utilise un context manager pour s'assurer que la session est correctement fermée
    après utilisation.
    :return: un générateur de session SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()