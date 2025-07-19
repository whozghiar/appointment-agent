"""Routes liées à la transcription vocale."""

import os
import httpx
from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from pathlib import Path
import uuid

# Création d’un routeur pour les endpoints liés à la reconnaissance vocale (STT)
router = APIRouter(prefix="/stt", tags=["STT"])

WHISPER_URL = os.getenv("WHISPER_URL", "http://localhost:8081/transcrire")  # adresse du conteneur dans le réseau docker-compose

@router.post("/transcrire")
async def transcrire_fichier_audio(file: UploadFile = File(...)):
    """
    Reçoit un fichier audio, le sauvegarde temporairement,
    puis le transmet à l’API du service Whisper via HTTP.
    Supprime ensuite le fichier local.

    :param file: fichier audio envoyé (UploadFile)
    :return: dictionnaire contenant le texte transcrit
    """
    temp_path = None  # Pour s'assurer que temp_path est défini dans le bloc finally
    try:
        # Génère un nom de fichier unique pour éviter les conflits
        temp_filename = f"temp_{uuid.uuid4().hex}.wav"
        temp_path = Path("temp") / temp_filename
        temp_path.parent.mkdir(parents=True, exist_ok=True)

        # Enregistre le fichier localement
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Transmet le fichier à Whisper (conteneur) via HTTP multipart
        with temp_path.open("rb") as audio_file:
            files = {"file": (temp_filename, audio_file, "audio/wav")}
            async with httpx.AsyncClient() as client:
                response = await client.post(WHISPER_URL, files=files)

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erreur du service STT distant")

        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)
