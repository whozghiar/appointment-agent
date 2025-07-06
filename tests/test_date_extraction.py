from backend.app.services.llm_reformulation import reformuler_avec_date_explicite
from backend.app.services.date_extraction import parser_date_depuis_texte

def test_date_simple():
    texte = "je voudrais un rendez-vous demain à 14h"
    reformulation = reformuler_avec_date_explicite(texte)
    dt = parser_date_depuis_texte(reformulation)
    assert dt is not None
    assert dt.hour == 14

def test_date_jour_nom():
    texte = "mardi à 9h30"
    reformulation = reformuler_avec_date_explicite(texte)
    dt = parser_date_depuis_texte(reformulation)
    assert dt is not None
    assert dt.hour == 9
    assert dt.minute == 30

def test_absence_date():
    texte = "je veux un rendez-vous bientôt"
    reformulation = reformuler_avec_date_explicite(texte)
    dt = parser_date_depuis_texte(reformulation)
    assert dt is None
