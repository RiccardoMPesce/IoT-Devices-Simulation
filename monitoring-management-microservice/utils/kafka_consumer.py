from aiokafka import AIOKafkaConsumer

from utils.logger import logger_config

from config import get_config

logger = logger_config(__name__)

configs = get_config()

def get_consumer() -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        configs["KAFKA_TOPICS"],
        bootstrap_servers=configs["KAFKA_INSTANCE"]
    )

async def consume():
    pass

