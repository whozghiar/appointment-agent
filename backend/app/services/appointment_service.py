from sqlalchemy.orm import Session
from backend.app.models.appointment_model import Appointment
from backend.app.schemas.appointment_schema import AppointmentCreate

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
