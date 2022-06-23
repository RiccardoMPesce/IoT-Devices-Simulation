import asyncio
import uvicorn
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.mqtt import fast_mqtt
from utils.config import get_config
from utils.logger import logger_config
from api.endpoint import endpoint
from db.database import database, Record
from utils.mqtt import handle_measure
from utils.kafka import kafka_init, consume


logger = logger_config(__name__)
settings = get_config()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, description=settings.DESCRIPTION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(endpoint)

# Init MQTT
fast_mqtt.init_app(app)

app.state.database = database


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
    
    payload = json.loads(payload)
    
    if "measure" in payload:
        await handle_measure(payload)
    
    return payload

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    logger.info(f"Client {client} disconnected")
    logger.info(f"Packet: {packet}")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    logger.info(f"Client {client} subscribed with QoS {qos}")
    logger.info(f"MID {mid}")
    logger.info(f"Properties {properties}")


@app.on_event("startup")
async def startup_event():
    database_ = app.state.database
    if not database_.is_connected:
        await database.connect()
    asyncio.create_task(kafka_init())
    asyncio.create_task(consume())
        
@app.on_event("shutdown")
async def shutdown_event():
    database_ = app.state.database
    if database_.is_connected:
        await database.disconnect()
    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8001)