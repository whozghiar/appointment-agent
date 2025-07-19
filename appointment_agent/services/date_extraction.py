"""Extraction de dates à partir de textes en langage naturel."""

from datetime import datetime
from dateutil.parser import parse
from typing import Optional


def parser_date_depuis_texte(texte: str) -> Optional[datetime]:
    """Retourne un ``datetime`` si une date est détectée."""
    try:
        return parse(texte, fuzzy=True)
    except Exception:
        return None
