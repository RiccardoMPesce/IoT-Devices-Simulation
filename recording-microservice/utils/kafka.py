import asyncio
import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from utils.config import get_config
from utils.logger import logger_config

settings = get_config()

logger = logger_config(__name__)

async def consume():
    kafka_topics = settings.KAFKA_TOPICS.split(",")

    loop = asyncio.get_event_loop()

    consumer = AIOKafkaConsumer(
        *kafka_topics, 
        loop=loop,
        bootstrap_servers=settings.KAFKA_INSTANCE 
        # group_id=settings.KAFKA_CONSUMER_GROUP
    )
    await consumer.start()
    try:
        async for msg in consumer:
            # logger.info(f"Consumed: {msg}")
            packet = {
                "topic": msg.topic,
                "partition": msg.partition,
                "timestamp": msg.timestamp,
                "payload": json.loads(msg.value)
            }
            logger.info("Consumed " + str(packet["payload"]))
    finally:
        await consumer.stop()


async def send_recording(recording: dict):
    kafka_topic = "measure_recordings"

    loop = asyncio.get_event_loop()

    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=settings.KAFKA_INSTANCE
    )
    await producer.start()

    payload = json.dumps(recording).encode("utf-8")
    
    try:
        await producer.send(topic=kafka_topic, value=payload)
    finally:
        await producer.stop()

