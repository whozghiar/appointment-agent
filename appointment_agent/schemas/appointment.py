"""Schémas Pydantic pour les rendez-vous."""

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AppointmentCreate(BaseModel):
    """Données requises pour créer un rendez-vous."""

    nom: str
    sexe: str
    telephone: str
    date: datetime
    prestation: str


class AppointmentRead(AppointmentCreate):
    """Rendez-vous avec identifiant."""

    id: int


model_config = ConfigDict(from_attributes=True)
