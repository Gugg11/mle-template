import json
import os
from kafka import KafkaProducer

def get_producer():
    bootstrap_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks='all',
        retries=3
    )

def send_prediction_message(features: list, prediction: int):
    """Отправляет сообщение в Kafka с признаками и предсказанием."""
    producer = get_producer()
    topic = os.environ.get("KAFKA_TOPIC", "predictions")
    message = {
        "features": features,
        "prediction": prediction
    }
    producer.send(topic, value=message)
    producer.flush()   # чтобы отправить немедленно (в реальном проекте лучше не вызывать flush каждый раз)