"""Configuration de l'application.

Chargée automatiquement depuis le fichier .env à la racine du projet.
"""
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Paramètres de l'application basés sur Pydantic."""
    database_url: str = "postgresql://user:pass@localhost:5433/appointments"
    whisper_url: str = "http://localhost:8081/transcrire"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    """Renvoie une instance unique des paramètres."""
    return Settings()
