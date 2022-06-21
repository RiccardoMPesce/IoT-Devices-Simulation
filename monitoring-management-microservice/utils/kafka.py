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
                "payload": msg.value.decode("utf-8") 
            }
            logger.info("Consumed " + packet["payload"])
    finally:
        await consumer.stop()


async def kafka_init():
    kafka_topics = settings.KAFKA_TOPICS.split(",")

    loop = asyncio.get_event_loop()

    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=settings.KAFKA_INSTANCE
    )
    await producer.start()
    try:
        for topic in kafka_topics:
            logger.info(f"Creating topic {topic} with test data")
            value_json = json.dumps({topic: "up"}).encode("utf-8")
            await producer.send_and_wait(topic=topic, value=value_json)
    finally:
        await producer.stop()