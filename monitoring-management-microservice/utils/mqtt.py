from utils.config import get_config
from utils.logger import logger_config

from fastapi_mqtt.config import MQTTConfig
from fastapi_mqtt.fastmqtt import FastMQTT

settings = get_config()

logger = logger_config(__name__)

mqtt_config = MQTTConfig(
    host=settings.MQTT_BROKER_HOST,
    port=settings.MQTT_BROKER_PORT
)

fast_mqtt = FastMQTT(
    config=mqtt_config,
    clean_session=False
)
