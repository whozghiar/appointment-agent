# Agent vocal de prise de rendez-vous – Coiffeur

Ce projet propose un agent conversationnel vocal permettant à un client de prendre rendez-vous chez un coiffeur. Il fonctionne localement grâce à Docker et des composants open source.

## Objectif
Automatiser la prise de rendez-vous par téléphone avec reconnaissance vocale, détection d'intention et stockage en base de données.

## Architecture

- **`backend/app`** : code Python principal (FastAPI, services et modèles).
- **`whisper`** : service de transcription audio.
- **`tts`** : service de synthèse vocale.
- **`asterisk`** : passerelle téléphonique.

Chaque service possède son propre Dockerfile.

## Lancer le projet

```bash
docker-compose build
docker-compose up
```

Une fois lancé, l'API FastAPI est disponible sur `http://localhost:8000`.

## Exemple minimal

```python
from backend.app.main import app
```

La configuration se fait via les variables du fichier `.env` à la racine.
