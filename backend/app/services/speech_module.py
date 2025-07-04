import whisper
from pathlib import Path

# Charge une fois le modèle Whisper
model = whisper.load_model("base")

def transcrire_audio(fichier_audio: str) -> str:
    """
    Transcrit un fichier audio en texte à l’aide de Whisper.
    :param fichier_audio: chemin vers un fichier .wav ou .mp3
    :return: transcription textuelle
    """
    if not Path(fichier_audio).is_file():
        raise FileNotFoundError(f"Fichier non trouvé : {fichier_audio}")

    result = model.transcribe(fichier_audio, language="fr")
    return result["text"]
