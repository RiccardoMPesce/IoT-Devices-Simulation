from utils.config import get_config
from utils.logger import logger_config
from db.database import database, Record

from fastapi_mqtt.config import MQTTConfig
from fastapi_mqtt.fastmqtt import FastMQTT
from datetime import datetime

settings = get_config()

logger = logger_config(__name__)

mqtt_config = MQTTConfig(
    host=settings.MQTT_BROKER_HOST,
    port=settings.MQTT_BROKER_PORT
)

fast_mqtt = FastMQTT(
    config=mqtt_config
)

# Handling measure utility
async def handle_measure(payload: dict):
    record = Record(
        device_id=payload["device_id"],
        measure=payload["measure"],
        value=payload["measure_value"],
        is_device_healthy=payload["health"],
        timestamp=datetime.fromtimestamp(payload["timestamp"])
    )
    await record.save()
    logger.info(f"Payload {payload} saved into database")
    return record
