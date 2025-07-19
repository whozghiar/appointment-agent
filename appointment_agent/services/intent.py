"""Gestion de l'intent de prise de rendez-vous."""

from datetime import datetime
from dateutil.parser import parse
from typing import Optional
import requests
import re


def send_reformulation_prompt(user_text: str) -> str:
    """Envoie le texte à un LLM local pour obtenir une date explicite."""
    today_str = datetime.today().strftime("%Y-%m-%d")
    prompt = (
        f"Aujourd'hui, nous sommes le {today_str}.\n"
        f"Reformule strictement la phrase suivante : « {user_text} »\n"
        "en remplaçant toute expression temporelle relative (\"demain\", \"mardi prochain\", \"dans la semaine\", "
        "\"en fin de journée\", \"à 14h\", etc.) par une DATE ET HEURE explicites au FORMAT UNIQUE :\n"
        "YYYY-MM-DD HH:mm\n"
        "- réponse EXACTE, sans mot supplémentaire,\n"
        "- sans préposition ni guillemets,\n"
        "- minutes toujours sur deux chiffres.\n"
        "Si aucune date/heure n’est détectable, répondre exactement :\n"
        "Aucune date détectée"
    )
    resp = requests.post(
        "http://localhost:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "mistralai/mistral-7b-instruct-v0.3",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Erreur API LM Studio : {resp.text}")
    content = resp.json()["choices"][0]["message"]["content"].strip()
    if (content.startswith('"') and content.endswith('"')) or (content.startswith("'") and content.endswith("'")):
        content = content[1:-1]
    return content


def extract_iso_from_text(text: str) -> Optional[str]:
    """Extrait un timestamp ISO d'une chaîne."""
    m = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", text)
    return m.group(0) if m else None


def reformulate_with_explicit_date(user_text: str) -> str:
    """Renvoie un timestamp ISO ou un message demandant plus de précision."""
    raw = send_reformulation_prompt(user_text)
    iso = extract_iso_from_text(raw)
    return iso if iso else "Veuillez préciser la date et l'heure pour votre rendez-vous"


def extract_datetime(text: str) -> Optional[datetime]:
    """Convertit un timestamp ISO en ``datetime``."""
    try:
        return parse(text, fuzzy=True)
    except Exception:
        return None


def detect_intent_and_datetime(transcribed_text: str) -> Optional[datetime]:
    """Détecte la date voulue à partir du texte transcrit."""
    reformulated = reformulate_with_explicit_date(transcribed_text)
    if "Veuillez préciser la date" in reformulated:
        return None
    return extract_datetime(reformulated)
