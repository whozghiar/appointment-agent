"""Orchestrateur de la prise de rendez-vous.

Coordonne la transcription, la détection d'intention et la planification.
"""
from datetime import datetime
from appointment_agent.services.intent import detect_intent_and_datetime
from appointment_agent.services.appointment import plan_appointment_if_available
from appointment_agent.utils.database import get_db
from appointment_agent.schemas.appointment import AppointmentCreate


def process_conversation(audio_path: str) -> AppointmentCreate | None:
    """Traite un fichier audio et crée un rendez-vous si possible.

    Exemple d'usage ::

        from appointment_agent.core.orchestrator import process_conversation
        rdv = process_conversation("/path/to/audio.wav")
        if rdv:
            print("Rendez-vous planifié", rdv.id)
    """
    # Transcription fictive : à remplacer par l'appel réel au service STT
    transcribed = "je veux un rendez-vous demain à 10h"
    date = detect_intent_and_datetime(transcribed)
    if not date:
        return None

    donnees = AppointmentCreate(
        nom="Client",
        sexe="H",
        telephone="0000000000",
        date=date,
        prestation="Coupe"
    )
    with get_db() as db:
        return plan_appointment_if_available(db, donnees)
