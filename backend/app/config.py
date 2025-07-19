"""Configuration de l'application.

Ce module charge les variables d'environnement depuis le fichier ``.env``.
Il expose la classe :class:`Settings` basée sur ``BaseSettings``.

Exemple d'utilisation::

    from backend.app.config import settings
    print(settings.POSTGRES_DB)
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Paramètres chargés depuis le fichier ``.env``."""

    POSTGRES_DB: str = "appointments"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "pass"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5433"

    class Config:
        env_file = ".env"


settings = Settings()
