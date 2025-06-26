# Dockerfile for Python batch producer and consumer
FROM python:3.10-slim

WORKDIR /app

COPY producer.py ./
COPY consumer.py ./
COPY requirements.txt ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
