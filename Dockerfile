FROM python:3.9-slim

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY main.py .

# FORZAMOS LA VERSIÓN 1.0.3 DE MOVIEPY QUE ES ESTABLE
RUN pip install fastapi uvicorn moviepy==1.0.3 python-multipart

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
