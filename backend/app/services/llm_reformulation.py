from datetime import datetime
import requests

def reformuler_avec_date_explicite(texte_utilisateur: str) -> str:
    """
    Envoie une requête au LLM local (via LM Studio) pour reformuler une phrase en remplaçant
    toute expression temporelle relative par une date et une heure explicites.

    :param texte_utilisateur: Exemple : "je veux un rendez-vous demain à 14h"
    :return: Exemple : "je veux un rendez-vous le 2025-07-06 à 14:00"
             ou "Aucune date détectée" si aucune date claire n'est trouvée
    """
    date_aujourdhui = datetime.today().strftime("%Y-%m-%d")

    prompt = (
        f"Aujourd'hui, nous sommes le {date_aujourdhui}. "
        f"Reformule la phrase suivante : \"{texte_utilisateur}\" "
        "en remplaçant toutes expressions temporelles (comme 'demain', 'mardi prochain', 'à 14h') "
        "par une date et une heure explicites au format strict suivant : YYYY-MM-DD HH:mm "
        "et uniquement si une date/heure est clairement exprimée. "
        "Sinon, répond exactement : 'Aucune date détectée'. "
        "Répond uniquement avec la phrase reformulée, sans ajout ni explication."
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

    return response.json()["choices"][0]["message"]["content"].strip()
