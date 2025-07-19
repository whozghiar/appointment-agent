"""Schémas Pydantic pour les rendez-vous."""

from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AppointmentCreate(BaseModel):
    nom: str
    sexe: str
    telephone: str
    date: datetime
    prestation: str

class AppointmentRead(AppointmentCreate):
    id: int

model_config = ConfigDict(from_attributes=True)
