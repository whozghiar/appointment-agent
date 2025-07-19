from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.appointment import Appointment

# Créneau d'ouverture par défaut
OUVERTURE = 9
FERMETURE = 18

def isAvailable(db: Session, date: datetime, duree_minutes: int) -> bool:
    """
    Vérifie si un créneau horaire est disponible dans la base existante.
    """
    debut = date
    fin = date + timedelta(minutes=duree_minutes)

    if debut.hour < OUVERTURE or fin.hour >= FERMETURE:
        return False

    rdvs = db.query(Appointment).all()
    for rdv in rdvs:
        rdv_debut = rdv.date
        rdv_fin = rdv.date + timedelta(minutes=30)  # durée fixe pour l’instant

        # Chevauchement
        if debut < rdv_fin and fin > rdv_debut:
            return False

    return True
