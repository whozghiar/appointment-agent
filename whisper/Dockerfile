FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install git+https://github.com/openai/whisper.git

CMD ["python3", "-m", "http.server", "8080"]
