from backend.app.services.date_extraction import extraire_date_heure

def test_date_simple():
    texte = "je voudrais un rendez-vous demain à 14h"
    dt = extraire_date_heure(texte)
    assert dt is not None
    assert dt.hour == 14

def test_date_jour_nom():
    texte = "mardi à 9h30"
    dt = extraire_date_heure(texte)
    assert dt is not None
    assert dt.hour == 9 and dt.minute == 30

def test_absence_date():
    texte = "je veux un rendez-vous bientôt"
    dt = extraire_date_heure(texte)
    assert dt is None or isinstance(dt, type(None))
