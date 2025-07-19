"""Point d'entrée de l'application FastAPI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from appointment_agent.api import stt, appointment
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
    return {"status": "ok"}
