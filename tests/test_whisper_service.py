import requests
from pathlib import Path
import io

WHISPER_URL = "http://localhost:8081/transcrire"


def test_transcription_valide():
    """
    Test standard : envoie un vrai fichier .wav au conteneur Whisper.
    Vérifie que la transcription est retournée et non vide.
    """
    audio_path = Path("tests/assets/test.wav")
    assert audio_path.exists(), "Fichier audio de test introuvable"

    with audio_path.open("rb") as f:
        files = {"file": ("test.wav", f, "audio/wav")}
        response = requests.post(WHISPER_URL, files=files)

    assert response.status_code == 200
    data = response.json()
    assert "transcription" in data
    assert isinstance(data["transcription"], str)
    assert len(data["transcription"].strip()) > 0


def test_fichier_audio_invalide():
    """
    Teste le comportement en envoyant un fichier corrompu.
    On attend une erreur HTTP 500 (transcription impossible).
    """
    fake_audio = io.BytesIO(b"not real audio")
    files = {"file": ("fake.wav", fake_audio, "audio/wav")}
    response = requests.post(WHISPER_URL, files=files)

    assert response.status_code == 500
    assert "detail" in response.json()


def test_format_non_audio():
    """
    Envoie un fichier texte au lieu d’un audio.
    Le serveur doit retourner une erreur 500 (invalid input).
    """
    text_file = io.BytesIO(b"je ne suis pas un audio")
    files = {"file": ("test.txt", text_file, "text/plain")}
    response = requests.post(WHISPER_URL, files=files)

    assert response.status_code == 500
    assert "detail" in response.json()


def test_absence_de_fichier():
    """
    Envoie une requête sans champ 'file'.
    Le serveur doit répondre avec 422 (FastAPI : champ requis manquant).
    """
    response = requests.post(WHISPER_URL, files={})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"


def test_taille_fichier_zero():
    """
    Envoie un fichier vide (0 octets).
    Whisper doit échouer et renvoyer une erreur 500.
    """
    empty_file = io.BytesIO(b"")
    files = {"file": ("empty.wav", empty_file, "audio/wav")}
    response = requests.post(WHISPER_URL, files=files)

    assert response.status_code == 500
    assert "detail" in response.json()
