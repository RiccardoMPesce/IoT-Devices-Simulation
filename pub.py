from aiokafka import AIOKafkaProducer
import asyncio

loop = asyncio.get_event_loop()

producer = AIOKafkaProducer(bootstrap_servers="localhost:9093", loop=loop)

for _ in range(100):
    producer.send("test", b"Test")