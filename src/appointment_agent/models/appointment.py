"""Définition du modèle SQLAlchemy des rendez-vous."""

from sqlalchemy import Column, Integer, String, DateTime
from appointment_agent.utils.database import Base

class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    sexe = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    prestation = Column(String, nullable=False)
