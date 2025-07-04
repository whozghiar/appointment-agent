import pytest
from backend.app.services.speech_module import transcrire_audio
from pathlib import Path

def test_transcription_fichier_existant():
    audio_path = Path("tests/assets/test.wav")
    assert audio_path.exists(), "Le fichier audio de test est manquant"

    texte = transcrire_audio(str(audio_path))
    print(f"Texte transcrit : {texte}")
    assert isinstance(texte, str)
    assert len(texte.strip()) > 0

def test_transcription_fichier_inexistant():
    with pytest.raises(FileNotFoundError):
        transcrire_audio("tests/assets/fichier_inexistant.wav")
