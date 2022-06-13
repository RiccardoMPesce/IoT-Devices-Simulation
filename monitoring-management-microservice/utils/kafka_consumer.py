from aiokafka import AIOKafkaConsumer

from utils.logger import logger_config

from config import get_config

logger = logger_config(__name__)

configs = get_config()

def get_device_consumer() -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        configs.KAFKA_TOPIC_DEVICES,
        bootstrap_servers=configs.KAFKA_INSTANCE
    )

async def consume():
    device_consumer = get_device_consumer()
    await device_consumer.start()
    while True:
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

