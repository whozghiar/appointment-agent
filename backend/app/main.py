from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import stt_router, appointment_router
app = FastAPI(title="Agent Prise de Rendez-vous Coiffeur")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stt_router.router)
app.include_router(appointment_router.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
