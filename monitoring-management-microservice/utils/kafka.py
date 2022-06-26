import asyncio
import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from utils.config import get_config
from utils.logger import logger_config
from db.common import db
from models.device_schema import UpdateDevice

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
            
            if packet["topic"] == "device_commands" and "device_id" in packet["payload"]:
                await handle_command(packet["payload"])
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
            # logger.info(f"Creating topic {topic} with test data")
            value_json = json.dumps({topic: "monitoring-management-microservice up"}).encode("utf-8")
            # await producer.send_and_wait(topic=topic, value=value_json)
    finally:
        await producer.stop()


async def handle_command(command: dict) -> dict:
    logger.info(str(command))
    update_dict = {
        "device_id": command["device_id"],
        "status": command["status"]
    }
    payload = UpdateDevice.parse_obj(update_dict)
    logger.info(f"Shutting down {str(update_dict)}")
    await db.device_update_one(payload)
    new_device = await db.device_get_one(update_dict["device_id"])
    return new_device
