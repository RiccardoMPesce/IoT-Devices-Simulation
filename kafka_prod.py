from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

producer.send("test", b"Hello")