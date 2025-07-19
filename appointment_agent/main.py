"""Point d'entrée FastAPI pour l'agent de rendez-vous."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import appointment, stt

app = FastAPI(title="Agent Prise de Rendez-vous Coiffeur")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stt.router)
app.include_router(appointment.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Vérifie que l'application fonctionne."""
    return {"status": "ok"}

