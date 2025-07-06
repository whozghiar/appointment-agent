from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from pydantic import ValidationError

from backend.app.main import app
from backend.app.models.appointment_model import Appointment
from backend.app.schemas.appointment_schema import AppointmentCreate
from backend.app.services.appointment_service import (
    creer_appointment,
    lister_appointments,
    recuperer_appointment,
    supprimer_appointment,
)
from backend.app.database import get_db

client = TestClient(app)


# --- SCHEMA TESTS ---
def test_schema_creation_valid():
    data = {
        "nom": "Alice",
        "sexe": "F",
        "telephone": "0600000000",
        "date": datetime.now().isoformat(),
        "prestation": "Shampoing"
    }
    obj = AppointmentCreate(**data)
    assert obj.nom == "Alice"
    assert obj.sexe == "F"

def test_schema_creation_invalid():
    try:
        AppointmentCreate(nom="Bob", sexe="X", telephone="bad", date="invalid", prestation="")
    except ValidationError as e:
        assert len(e.errors()) > 0


# --- MODEL TESTS ---
def test_model_instantiation():
    a = Appointment(
        nom="Test",
        sexe="H",
        telephone="0700000000",
        date=datetime.now(),
        prestation="Coupe"
    )
    assert a.nom == "Test"
    assert a.prestation == "Coupe"


# --- SERVICE TESTS ---
def test_service_create_and_fetch():
    with get_db() as db:
        payload = AppointmentCreate(
            nom="ServiceTest",
            sexe="F",
            telephone="0611223344",
            date=datetime.now() + timedelta(days=1),
            prestation="Brushing"
        )
        a = creer_appointment(db, payload)
        assert a.id is not None
        fetched = recuperer_appointment(db, a.id)
        assert fetched is not None
        assert fetched.nom == "ServiceTest"

def test_service_delete():
    with get_db() as db:
        payload = AppointmentCreate(
            nom="ToDelete",
            sexe="H",
            telephone="0699887766",
            date=datetime.now() + timedelta(days=2),
            prestation="Coloration"
        )
        a = creer_appointment(db, payload)
        deleted = supprimer_appointment(db, a.id)
        assert deleted is not None
        assert deleted.nom == "ToDelete"

def test_service_list():
    with get_db() as db:
        payload1 = AppointmentCreate(
            nom="ListTest1",
            sexe="F",
            telephone="0688776655",
            date=datetime.now() + timedelta(days=3),
            prestation="Soin"
        )
        payload2 = AppointmentCreate(
            nom="ListTest2",
            sexe="H",
            telephone="0677665544",
            date=datetime.now() + timedelta(days=4),
            prestation="Coupe"
        )
        creer_appointment(db, payload1)
        creer_appointment(db, payload2)

        appointments = lister_appointments(db)
        assert len(appointments) >= 2
        assert any(a.nom == "ListTest1" for a in appointments)
        assert any(a.nom == "ListTest2" for a in appointments)


# --- ROUTER TESTS ---
def test_router_create_and_read_and_delete():
    data = {
        "nom": "RouterTest",
        "sexe": "F",
        "telephone": "0612345678",
        "date": (datetime.now() + timedelta(days=1)).isoformat(),
        "prestation": "Soin"
    }

    res = client.post("/appointments/", json=data)
    assert res.status_code == 200
    appointment_id = res.json()["id"]

    res = client.get(f"/appointments/{appointment_id}")
    assert res.status_code == 200
    assert res.json()["nom"] == "RouterTest"

    res = client.delete(f"/appointments/{appointment_id}")
    assert res.status_code == 200
    assert res.json()["nom"] == "RouterTest"
