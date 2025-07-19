"""Orchestre la conversation pour planifier un rendez-vous."""

from datetime import datetime
from sqlalchemy.orm import Session

from ..services import intent, appointment
from ..utils.database import get_db


def process_conversation(audio_path: str) -> datetime | None:
    """Traite un fichier audio puis crée un rendez-vous si possible."""
    transcription = stt_transcribe(audio_path)
    dt = intent.detect_intent_and_datetime(transcription)
    if dt is None:
        return None
    with get_db() as db:
        payload = appointment.AppointmentCreate(
            nom="Client", sexe="U", telephone="000", date=dt, prestation="Coupe"
        )
        appointment.plan_appointment_if_available(db, payload)
    return dt


def stt_transcribe(path: str) -> str:
    """Exemple simplifié de transcription du fichier."""
    from . import stt_service  # type: ignore
    return stt_service.transcribe(path)
