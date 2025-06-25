# Dockerfile for Python producer and consumer
FROM python:3.10-slim

WORKDIR /app

COPY producer.py ./
COPY consumer.py ./

# Install dependencies if requirements.txt exists
COPY requirements.txt ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

CMD ["python", "producer.py"]
