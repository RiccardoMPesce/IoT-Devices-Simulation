import asyncio
import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from utils.config import get_config
from utils.logger import logger_config
from db.database import Record

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
            if packet["topic"] == "measure_rollback":
                await rollback_recording(packet["payload"]["record_id"])
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


async def send_command(command: dict):
    kafka_topic = "device_commands"

    loop = asyncio.get_event_loop()

    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=settings.KAFKA_INSTANCE
    )
    await producer.start()

    payload = json.dumps(command).encode("utf-8")
    
    try:
        await producer.send(topic=kafka_topic, value=payload)
    finally:
        await producer.stop()

async def rollback_recording(recording_id: int):
    logger.info(f"Recording Microservide: executing rollback {recording_id}")
    await Record.objects.delete(recording_id=recording_id)

