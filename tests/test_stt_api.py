import pytest
from fastapi.testclient import TestClient
from appointment_agent.main import app
from pathlib import Path

client = TestClient(app)

def test_transcrire_endpoint_ok():
    """
    Teste l'endpoint /stt/transcrire avec un vrai fichier audio.
    Vérifie que :
    - Le code HTTP est 200
    - La transcription est présente, non vide, et bien une string
    """
    audio_path = Path("tests/assets/test.wav")
    with audio_path.open("rb") as f:
        files = {"file": ("test.wav", f, "audio/wav")}
        response = client.post("/stt/transcrire", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "transcription" in data
    assert isinstance(data["transcription"], str)
    assert len(data["transcription"].strip()) > 0

def test_transcrire_endpoint_mauvais_format():
    """
    Teste la réaction de l'API quand on envoie un fichier au mauvais format.
    L’API doit répondre avec une erreur 500, car Whisper échouera à interpréter les données.
    """
    response = client.post("/stt/transcrire", files={"file": ("test.txt", b"not audio", "text/plain")})
    assert response.status_code == 500
