from utils.config import get_config

from fastapi_mqtt.config import MQTTConfig
from fastapi_mqtt.fastmqtt import FastMQTT

settings = get_config()

mqtt_config = MQTTConfig(
    host=settings.MQTT_BROKER_HOST
)

fast_mqtt = FastMQTT(
    config=mqtt_config
)