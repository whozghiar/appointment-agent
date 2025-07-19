"""Orchestre la conversation entre l'utilisateur et les services."""

from ..services import intent, availability, appointment
from ..utils.database import get_db
from ..schemas.appointment import AppointmentCreate


def process_conversation(text: str) -> str:
    """Exemple de pipeline très simplifié."""
    date = intent.detect_intent_and_datetime(text)
    if date is None:
        return "Veuillez préciser la date et l'heure."

    with get_db() as db:
        if availability.isAvailable(db, date, 30):
            data = AppointmentCreate(
                nom="Client", sexe="F", telephone="0000000000", date=date, prestation="Coupe"
            )
            appointment.creer_appointment(db, data)
            return "Rendez-vous confirmé"
        return "Créneau indisponible"
