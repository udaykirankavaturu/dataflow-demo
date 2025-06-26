import time
import json
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from datetime import datetime
import random

# --- RETRY LOGIC ---
producer = None
retries = 5
while retries > 0:
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:29092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Successfully connected to Kafka.")
        break
    except NoBrokersAvailable:
        print(f"Kafka not available, retrying in 5 seconds... ({retries} retries left)")
        retries -= 1
        time.sleep(5)

if not producer:
    print("Could not connect to Kafka after several retries. Exiting.")
    exit(1)
# --- END RETRY LOGIC ---

topic_name = 'batch-news'
news_items = [
    "[Batch News] Market closes for the week",
    "[Batch Weather] Weekly forecast released",
    "[Batch Tech] Major software update available",
    "[Batch Sports] Season summary published"
]

batch_size = 10
batch = []
print("Starting batch producer...")
for i in range(batch_size):
    message = {
        'message': f"{random.choice(news_items)} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        'id': i
    }
    batch.append(message)
    print(f"Prepared: {message}")

# Send the batch as individual messages (Kafka does not support batch send natively)
for msg in batch:
    producer.send(topic_name, msg)
    print(f"Sent: {msg}")
producer.flush()
print("Batch sent. Exiting.")
