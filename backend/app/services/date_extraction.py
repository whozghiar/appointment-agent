from datetime import datetime
from dateutil.parser import parse
from typing import Optional
import requests

def parser_date_depuis_texte(texte: str) -> Optional[datetime]:
    """
    Tente d'extraire un datetime depuis n'importe quelle chaîne contenant une date et heure.
    Ne repose plus sur un format fixe.

    :param texte: chaîne en langage naturel contenant potentiellement une date
    :return: objet datetime ou None si parsing impossible
    """
    try:
        return parse(texte, fuzzy=True)
    except Exception:
        return None

