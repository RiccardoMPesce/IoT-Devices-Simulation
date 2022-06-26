import uvicorn
import asyncio
import json 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.config import get_config
from db.common import db
from api.endpoint import endpoint
from utils.logger import logger_config
from utils.mqtt import fast_mqtt
from utils.kafka import kafka_init, consume

settings = get_config()

logger = logger_config(__name__)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, description=settings.DESCRIPTION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including routes
app.include_router(endpoint)

# MQTT
fast_mqtt.init_app(app)

# Add Prometheus

logger.info("API launched for " + settings.ENVIRONMENT + " environment")


@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    logger.info(f"Client {str(client)} connected to {settings.MQTT_BROKER_HOST}")
    logger.info(f"Flags: {str(flags)}")
    logger.info(f"RC: {str(rc)}")
    logger.info(f"Properties: {str(properties)}")
    logger.info(f"Now subscribing to measure related topics under {settings.MQTT_TOPIC_PREFIX}#")
    fast_mqtt.client.subscribe(settings.MQTT_TOPIC_PREFIX + "#", qos=1)

@fast_mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    logger.info(f"Client {str(client)} received message from topic {topic} with QoS {qos}")
    logger.info(f"Payload: {str(payload)}")
    logger.info(f"Properties: {str(properties)}")
    
    return json.loads(payload)

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    logger.info(f"Client {client} disconnected")
    logger.info(f"Packet: {packet}")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    logger.info(f"Client {client} subscribed with QoS {qos}")
    logger.info(f"MID {mid}")
    logger.info(f"Properties {properties}")

# Startup event routine
@app.on_event("startup")
async def startup():
    logger.info("Application startup")
    await db.connect_to_database(path=settings.DB_URI, db_name=settings.DB_NAME)
    # asyncio.create_task(kafka_init())
    asyncio.create_task(consume())

# Shutdown event routine
@app.on_event("shutdown")
async def shutdown():
    logger.info("Application shutdown")
    await db.close_database_connection()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)