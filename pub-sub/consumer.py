import json
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import time

# --- RETRY LOGIC ---
consumer = None
retries = 5
while retries > 0:
    try:
        consumer = KafkaConsumer(
            'news',
            bootstrap_servers='kafka:29092',
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        print("Successfully connected to Kafka.")
        break # Exit loop if connection is successful
    except NoBrokersAvailable:
        print(f"Kafka not available, retrying in 5 seconds... ({retries} retries left)")
        retries -= 1
        time.sleep(5)

if not consumer:
    print("Could not connect to Kafka after several retries. Exiting.")
    exit(1)
# --- END RETRY LOGIC ---


print("Starting pub/sub consumer...")
for message in consumer:
    print(f"--> Received: {message.value['message']}")