"""Routes FastAPI pour la gestion des rendez-vous."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from appointment_agent.utils.database import get_db
from appointment_agent.schemas.appointment import AppointmentCreate, AppointmentRead
from appointment_agent.services import appointment as appointment_service

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("/", response_model=AppointmentRead)
def creer_rdv(donnees: AppointmentCreate, db: Session = Depends(get_db)):
    with get_db() as db:
        rdv = appointment_service.plan_appointment_if_available(db, donnees)
    if not rdv:
        raise HTTPException(status_code=400, detail="Erreur lors de la création du rendez-vous")
    return rdv

@router.get("/", response_model=list[AppointmentRead])
def lister_rdv(db: Session = Depends(get_db)):
    with get_db() as db:
        rdvs = appointment_service.lister_appointments(db)
    if not rdvs:
        raise HTTPException(status_code=404, detail="Aucun rendez-vous trouvé")
    return rdvs


@router.get("/{rdv_id}", response_model=AppointmentRead)
def lire_rdv(rdv_id: int, db: Session = Depends(get_db)):
    with get_db() as db:
        rdv = appointment_service.recuperer_appointment(db, rdv_id)
    if not rdv:
        raise HTTPException(status_code=404, detail="Rendez-vous introuvable")
    return rdv

@router.delete("/{rdv_id}", response_model=AppointmentRead)
def supprimer_rdv(rdv_id: int, db: Session = Depends(get_db)):
    with get_db() as db:
        rdv = appointment_service.supprimer_appointment(db, rdv_id)
    if not rdv:
        raise HTTPException(status_code=404, detail="Rendez-vous introuvable")
    return rdv
