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
    config=mqtt_config
)

@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    fast_mqtt.client.subscribe(settings.MQTT_TOPIC_PREFIX, qos=1)
    logger.info(f"Client {str(client)} connected to {settings.MQTT_BROKER_HOST}")
    logger.info(f"Subscribed to topic {settings.MQTT_TOPIC_PREFIX}")
    logger.info(f"Flags: {str(flags)}")
    logger.info(f"RC: {str(rc)}")
    logger.info(f"Properties: {str(properties)}")

@fast_mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    logger.info(f"Client {str(client)} received message from topic {topic} with QoS {qos}")
    logger.info(f"Payload: {str(payload)}")
    logger.info(f"Properties: {str(properties)}")
    
    return payload.decode("utf-8") 

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    logger.info(f"Client {client} disconnected")
    logger.info(f"Packet: {packet}")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    logger.info(f"Client {client} subscribed with QoS {qos}")
    logger.info(f"MID {mid}")
    logger.info(f"Properties {properties}")
