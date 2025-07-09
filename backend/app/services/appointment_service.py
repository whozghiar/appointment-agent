from http.client import HTTPException

from sqlalchemy.orm import Session
from backend.app.models.appointment_model import Appointment
from backend.app.schemas.appointment_schema import AppointmentCreate
from backend.app.services.availabilty_service import isAvailable

def creer_appointment(db: Session, donnees: AppointmentCreate) -> Appointment:
    appointment = Appointment(**donnees.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

def lister_appointments(db: Session):
    return db.query(Appointment).all()

def recuperer_appointment(db: Session, id_: int):
    return db.query(Appointment).filter(Appointment.id == id_).first()

def supprimer_appointment(db: Session, id_: int):
    appointment = recuperer_appointment(db, id_)
    if appointment:
        db.delete(appointment)
        db.commit()
    return appointment

def plan_appointment_if_available(db: Session, donnees: AppointmentCreate) -> Appointment:
    """
    Tente de créer un rendez-vous si le créneau est disponible.

    :param db: Session SQLAlchemy
    :param donnees: Données du rendez-vous proposé
    :return: Objet Appointment si succès, ou lève une exception HTTP 400
    """
    if isAvailable(db, donnees.date, 30):
        return creer_appointment(db, donnees)
    raise HTTPException(status_code=400, detail="Créneau indisponible")