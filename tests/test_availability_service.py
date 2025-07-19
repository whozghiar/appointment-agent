from datetime import datetime, timedelta
from appointment_agent.utils.database import SessionLocal
from appointment_agent.models.appointment import Appointment
from appointment_agent.services.availability import isAvailable

def test_disponibilite_sans_conflit():
    db = SessionLocal()
    date = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    assert isAvailable(db, date, 30)

def test_disponibilite_avec_conflit():
    db = SessionLocal()
    now = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
    rdv = Appointment(nom="Test", sexe="H", telephone="0000000000", date=now, prestation="Coupe")
    db.add(rdv)
    db.commit()

    conflit = isAvailable(db, now, 30)
    assert not conflit
    db.delete(rdv)
    db.commit()

def test_disponibilite_en_dehors_heures():
    db = SessionLocal()
    matin = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
    soir = datetime.now().replace(hour=18, minute=30, second=0, microsecond=0)
    assert not isAvailable(db, matin, 30)
    assert not isAvailable(db, soir, 30)
