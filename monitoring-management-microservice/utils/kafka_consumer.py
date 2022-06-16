from aiokafka import AIOKafkaConsumer

from utils.logger import logger_config

from config import get_config

logger = logger_config(__name__)

configs = get_config()

async def consume():
    topics_to_subscribe = configs.KAFKA_TOPICS.split(",")
    bootstrap_servers = configs.KAFKA_INSTANCE.split(",")
    logger.info(f"Bootstrapping from servers {bootstrap_servers}")
    logger.info(f"Subscribing to topics {topics_to_subscribe}")
    consumer = AIOKafkaConsumer(
        *topics_to_subscribe,
        bootstrap_servers=bootstrap_servers
    )
    logger.info(f"Consumer creation succeeded, now listening for new messages")
    await consumer.start()
    try:
        async for msg in consumer:
            payload = {
                "topic": msg["topic"],
                "partition": msg["partition"],
                "offset": msg["offset"],
                "key": msg["key"],
                "value": msg["value"],
                "timestamp": msg["timestamp"]
            }
            logger.info("Received ", str(payload))
    except Exception as exception:
        logger.info(f"Exception '{exception}' occurred")
    finally:
        await consumer.stop()

