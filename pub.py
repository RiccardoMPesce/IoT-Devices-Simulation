from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="localhost:9093")

for _ in range(100):
    producer.send("test", b"Test")