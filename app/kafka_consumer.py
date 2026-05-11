import json
import os
from kafka import KafkaConsumer

def main():
    bootstrap_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    topic = os.environ.get("KAFKA_TOPIC", "predictions")
    
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        group_id='ml-consumer-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    print(f"Kafka Consumer started. Listening on topic '{topic}'...")
    for message in consumer:
        print(f"Received: features={message.value['features']}, prediction={message.value['prediction']}")

if __name__ == "__main__":
    main()