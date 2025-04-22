FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#create directories for persistence
RUN mkdir -p ./chromadb
RUN mkdir -p ./data

#set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATABASE=/app/data/feedback.db
ENV CHROMA_PATH=/app/chromadb

#run gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT run:app