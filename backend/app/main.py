from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Agent Prise de Rendez-vous Coiffeur")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
