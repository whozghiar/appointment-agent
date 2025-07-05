from fastapi import FastAPI, UploadFile, File, HTTPException
import whisper
import shutil
from pathlib import Path
import uuid

model = whisper.load_model("base")
app = FastAPI(title="Whisper STT Service")

@app.post("/transcrire")
async def transcrire(file: UploadFile = File(...)):
    try:
        temp_filename = f"{uuid.uuid4().hex}.wav"
        path = Path("/tmp") / temp_filename

        with path.open("wb") as f:
            shutil.copyfileobj(file.file, f)

        result = model.transcribe(str(path), language="fr")
        path.unlink(missing_ok=True)
        return {"transcription": result["text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
