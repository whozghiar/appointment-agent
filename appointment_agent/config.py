"""Configuration de l'application chargée depuis l'environnement."""

from pydantic import BaseSettings

class Settings(BaseSettings):
    """Charge les variables depuis un fichier .env situé à la racine."""

    postgres_db: str = "appointments"
    postgres_user: str = "user"
    postgres_password: str = "pass"
    postgres_host: str = "localhost"
    postgres_port: str = "5433"

    class Config:
        env_file = ".env"

settings = Settings()
