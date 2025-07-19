"""Routes liées à la transcription vocale."""

import os
import shutil
import uuid
from pathlib import Path

import httpx
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(prefix="/stt", tags=["STT"])

WHISPER_URL = os.getenv("WHISPER_URL", "http://localhost:8081/transcrire")


@router.post("/transcrire")
async def transcrire_fichier_audio(file: UploadFile = File(...)):
    """Envoie le fichier audio au service Whisper et renvoie la transcription."""
    temp_path = None
    try:
        temp_filename = f"temp_{uuid.uuid4().hex}.wav"
        temp_path = Path("temp") / temp_filename
        temp_path.parent.mkdir(parents=True, exist_ok=True)

        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

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
