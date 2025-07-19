# Agent vocal de prise de rendez-vous – Coiffeur

Ce projet met en place un agent conversationnel téléphonique vocal permettant à un client de prendre rendez-vous chez un coiffeur. Il s'exécute en local via Docker, en utilisant des composants open-source et gratuits.

---

## Objectif

Automatiser la prise de rendez-vous via un appel vocal, avec reconnaissance de la parole, synthèse vocale, intégration Google Calendar, et envoi d'email de confirmation.

---

## Architecture des services

### 1. `backend` (FastAPI)
- Sert de cœur applicatif
- Gère la logique métier : dialogue, calendrier, communication
- Fournit des endpoints REST pour les futures extensions
- Exposé sur `http://localhost:8000`

### 2. `whisper` (Speech-to-Text)
- Utilise Whisper d’OpenAI pour convertir l’audio de l’appelant en texte
- Fonctionne en local via HTTP

### 3. `tts` (Text-to-Speech)
- Fournit la synthèse vocale à partir des textes renvoyés par le backend
- Implémentable avec Coqui.ai ou autre moteur local open-source

### 4. `asterisk` (VoIP)
- Route les appels téléphoniques vers le système local
- Interagit avec les scripts backend via AGI ou websocket
- Permet d’accueillir les appels, d’enregistrer les audios et de diffuser les réponses

---

## Démarrage

### Pré-requis

- Docker
- Docker Compose

### Lancer le projet

```bash
docker-compose build
docker-compose up
```

## Structure du code

```text
src/
    appointment_agent/
        api/            # Routes FastAPI
        core/           # Orchestrateur métier
        models/         # Modèles SQLAlchemy
        schemas/        # Schémas Pydantic
        services/       # Logique applicative
        utils/          # Outils divers
```
