# tests/test_intent_service.py

from datetime import datetime
import re
import pytest
from unittest.mock import patch, Mock
from backend.app.services.intent import (
    send_reformulation_prompt,
    extract_iso_from_text,
    reformulate_with_explicit_date,
    extract_datetime,
    detect_intent_and_datetime
)


def is_valid_iso_format(text: str) -> bool:
    """
    Vérifie si une date au format YYYY-MM-DD HH:mm est présente dans la chaîne.
    """
    return re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", text) is not None


def test_extract_iso_from_text_found():
    """
    Test non moqué : extraction ISO d'une chaîne contenant un timestamp.
    """
    texte = "Le rendez-vous est le 2025-07-20 13:45 pour vous."
    iso = extract_iso_from_text(texte)
    print("Date ISO extraite :", iso)
    assert iso == "2025-07-20 13:45"


def test_extract_iso_from_text_not_found():
    """
    Test non moqué : None si aucun timestamp présent.
    """
    texte = "Aucune date ici"
    iso = extract_iso_from_text(texte)
    print("Date ISO extraite (absente) :", iso)
    assert iso is None

@patch("backend.app.services.intent.requests.post")
def test_send_reformulation_prompt_moque(mock_post):
    """
    Test moqué : envoie du prompt et nettoyage des guillemets.
    """
    contenu = '"Prenez rendez-vous le 2025-07-21 10:30"'
    mock_resp = Mock(status_code=200)
    mock_resp.json.return_value = {"choices":[{"message":{"content":contenu}}]}
    mock_post.return_value = mock_resp

    result = send_reformulation_prompt("je veux un rendez-vous demain à 10h")
    print("Résultat brut prompt (mock) :", result)
    assert result == "Prenez rendez-vous le 2025-07-21 10:30"


def test_send_reformulation_prompt_reel():
    """
    Test réel non moqué : sollicite le LLM local pour reformulation.
    """
    phrase = "je veux un rendez-vous demain à 15h"
    resultat = send_reformulation_prompt(phrase)
    print("Résultat brut prompt (réel) :", resultat)
    # Vérifie que la réponse contient un timestamp ISO extractible ou indique l'absence de date
    assert isinstance(resultat, str)
    iso = extract_iso_from_text(resultat)
    print("Date ISO extraite du prompt réel :", iso)
    assert iso is not None or "Aucune date détectée" in resultat

@patch("backend.app.services.intent.send_reformulation_prompt")
def test_reformulate_with_explicit_date_moque(mock_prompt):
    """
    Test moqué : cas où le LLM renvoie un timestamp valide.
    """
    mock_prompt.return_value = "Ok c'est fixé au 2025-07-22 09:15"
    res = reformulate_with_explicit_date("je veux un rendez-vous")
    print("Résultat reformulation (mock) :", res)
    assert res == "2025-07-22 09:15"


def test_reformulate_with_explicit_date_reel():
    """
    Test réel non moqué : reformulation effective par le LLM.
    """
    phrase = "je veux un rendez-vous demain à 16h"
    res = reformulate_with_explicit_date(phrase)
    print("Résultat reformulation (réel) :", res)
    assert isinstance(res, str)
    assert is_valid_iso_format(res) or "Veuillez préciser" in res


def test_extract_datetime_valid():
    """
    Test non moqué : parsing ISO en datetime.
    """
    dt = extract_datetime("2025-08-01 12:00")
    print("Datetime parsé :", dt)
    assert isinstance(dt, datetime)
    assert (dt.year, dt.month, dt.day, dt.hour, dt.minute) == (2025, 8, 1, 12, 0)


def test_extract_datetime_invalid():
    """
    Test non moqué : None si absence de date.
    """
    dt = extract_datetime("aucune date ici")
    print("Datetime parsé (invalide) :", dt)
    assert dt is None

@patch("backend.app.services.intent.reformulate_with_explicit_date")
def test_detect_intent_and_datetime_success(mock_reform):
    """
    Test moqué : détection datetime valide via pipeline.
    """
    mock_reform.return_value = "2025-09-10 11:00"
    dt = detect_intent_and_datetime("prends rendez-vous")
    print("Datetime détectée (mock) :", dt)
    assert isinstance(dt, datetime)
    assert (dt.year, dt.month, dt.day, dt.hour, dt.minute) == (2025, 9, 10, 11, 0)

@patch("backend.app.services.intent.reformulate_with_explicit_date")
def test_detect_intent_and_datetime_none(mock_reform):
    """
    Test moqué : renvoie None si pas de date explicite.
    """
    mock_reform.return_value = "Veuillez préciser la date et l'heure pour votre rendez-vous"
    dt = detect_intent_and_datetime("prends rendez-vous bientôt")
    print("Datetime détectée (mock none) :", dt)
    assert dt is None
