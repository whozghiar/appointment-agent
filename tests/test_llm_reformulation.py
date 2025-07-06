from backend.app.services.llm_reformulation import reformuler_avec_date_explicite

def test_llm_reformulation_date_claire():
    texte = "je voudrais un rendez-vous demain à 14h"
    reformulation = reformuler_avec_date_explicite(texte)
    print("Reformulation:", reformulation)
    assert "2025" in reformulation and "14:00" in reformulation

def test_llm_reformulation_ambigue():
    texte = "je veux un rendez-vous bientôt"
    reformulation = reformuler_avec_date_explicite(texte)
    print("Reformulation:", reformulation)
    assert reformulation.strip() == "Aucune date détectée"
