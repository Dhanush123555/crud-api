FROM python:3.13.7-slim

WORKDIR /usr/src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app app

COPY main.py .

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn","--host", "0.0.0.0", "main:app"]