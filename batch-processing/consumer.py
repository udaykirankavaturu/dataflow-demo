print('hello from consumer', flush=True)
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
            'batch-news',
            bootstrap_servers='kafka:29092',
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        print("Successfully connected to Kafka.")
        break
    except NoBrokersAvailable:
        print(f"Kafka not available, retrying in 5 seconds... ({retries} retries left)")
        retries -= 1
        time.sleep(5)

if not consumer:
    print("Could not connect to Kafka after several retries. Exiting.")
    exit(1)
# --- END RETRY LOGIC ---

print("Starting batch consumer...")
timeout_seconds = 10  # Adjust as needed
start_time = time.time()
batch = []
batch_size = 10

while True:
    msg_pack = consumer.poll(timeout_ms=1000)
    if msg_pack:
        for tp, messages in msg_pack.items():
            for message in messages:
                batch.append(message.value)
                print(f"Received: {message.value}")
                if len(batch) == batch_size:
                    print(f"\nProcessing batch of {batch_size} messages:")
                    for msg in batch:
                        print(f"--> {msg}")
                    batch = []
                    print("Batch processed. Waiting for next batch...\n")
        start_time = time.time()  # Reset timer on message
    else:
        if time.time() - start_time > timeout_seconds:
            print(f"No messages received in {timeout_seconds} seconds. Exiting consumer loop.")
            break

if batch:
    print(f"\nProcessing final batch of {len(batch)} messages:")
    for msg in batch:
        print(f"--> {msg}")
    print("Final batch processed.")

consumer.close()
print("Consumer closed.")

