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
        break  # Exit loop if connection is successful
    except NoBrokersAvailable:
        print(f"Kafka not available, retrying in 5 seconds... ({retries} retries left)")
        retries -= 1
        time.sleep(5)

if not producer:
    print("Could not connect to Kafka after several retries. Exiting.")
    exit(1)
# --- END RETRY LOGIC ---


topic_name = 'news'
news_items = [
    "[Breaking News] Market hits an all-time high",
    "[Weather Update] Heavy rainfall expected in the southern regions",
    "[Tech News] New AI model released by a major tech firm",
    "[Sports] Local team wins the championship"
]

print("Starting pub/sub producer...")
count = 0
while True:
    message = f"{random.choice(news_items)} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    producer.send(topic_name, {'message': message})
    print(f"Sent: {message}")
    time.sleep(2)
    count += 1
    if count >= 10:  # Limit to 10 messages for demonstration
        break