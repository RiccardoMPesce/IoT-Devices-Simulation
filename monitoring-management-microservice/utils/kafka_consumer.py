from aiokafka import AIOKafkaConsumer

from utils.logger import logger_config

from config import get_config

logger = logger_config(__name__)

configs = get_config()

async def device_consume():
    device_consumer = AIOKafkaConsumer(
        *configs.KAFKA_TOPIC_DEVICES,
        bootstrap_servers=configs.KAFKA_INSTANCE
    )
    await device_consumer.start()
    try:
        async for msg in device_consumer:
            payload = {
                "topic": msg["topic"],
                "partition": msg["partition"],
                "offset": msg["offset"],
                "key": msg["key"],
                "value": msg["value"],
                "timestamp": msg["timestamp"]
            }
            logger.info("Received ", str(payload))
    finally:
        await device_consumer.stop()

