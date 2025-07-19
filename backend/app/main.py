"""Point d'entrée de l'application FastAPI.

Ce module crée l'instance :class:`FastAPI` et enregistre les routeurs
définis dans :mod:`backend.app.api`.

Exemple d'exécution::

    uvicorn backend.app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import appointment, stt

app = FastAPI(title="Agent Prise de Rendez-vous Coiffeur")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stt.router)
app.include_router(appointment.router)


@app.get("/health")
def health_check():
    """Vérifie que l'application répond."""
    return {"status": "ok"}
