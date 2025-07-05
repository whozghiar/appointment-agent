from datetime import datetime
import requests

def reformuler_avec_date_explicite(texte_utilisateur: str) -> str:
    """
    Envoie une requête à ton modèle LM Studio en précisant la date du jour
    et en demandant une reformulation explicite.

    :param texte_utilisateur: ex: "je veux un rendez-vous demain à 14h"
    :return: ex: "je veux un rendez-vous le 2025-07-06 à 14:00"
    """
    date_aujourdhui = datetime.today().strftime("%Y-%m-%d")

    prompt = (
        f"Aujourd'hui nous sommes le {date_aujourdhui}. "
        f"Reformule cette phrase : \"{texte_utilisateur}\" "
        "en remplaçant toute expression temporelle relative par une date et une heure explicites. "
        "Formate la date/heure comme `YYYY-MM-DD HH:mm`. "
        "Répond uniquement par la phrase reformulée."
    )

    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "mistralai/mistral-7b-instruct-v0.3",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    if response.status_code != 200:
        raise RuntimeError(f"Erreur API LM Studio : {response.text}")

    reformulation = response.json()["choices"][0]["message"]["content"].strip()
    return reformulation
