FROM python:3.9-slim

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY main.py .

RUN pip install fastapi uvicorn moviepy python-multipart

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
