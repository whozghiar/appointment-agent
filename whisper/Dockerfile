FROM python:3.11-slim

WORKDIR /app

# Installation système minimale
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    apt-get clean

# Install Whisper
RUN pip install git+https://github.com/openai/whisper.git

# API minimale en FastAPI
RUN pip install fastapi uvicorn python-multipart

COPY . .

CMD ["uvicorn", "whisper_api:app", "--host", "0.0.0.0", "--port", "8080"]
