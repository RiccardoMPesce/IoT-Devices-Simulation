from fastapi_mqtt.config import MQTTConfig
from fastapi_mqtt.fastmqtt import FastMQTT

mqtt_config = MQTTConfig(
    host="broker.hivemq.com"
)

fast_mqtt = FastMQTT(
    config=mqtt_config
)