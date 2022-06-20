import asyncio
import uvicorn

from fastapi import FastAPI

# CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
import kafka

# Used to add Prometheus support
from starlette_exporter import PrometheusMiddleware, handle_metrics

from config import get_config
from db.common import db
from api.endpoint import endpoint
from utils.logger import logger_config

from aiokafka import AIOKafkaConsumer
import kafka

from api.simulation_api import fast_mqtt

settings = get_config()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs"
)

# MQTT
fast_mqtt.init_app(app)

# Including routes
app.include_router(endpoint)

settings = get_config()

logger = logger_config(__name__)

# Add Prometheus
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

# Add CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("API launched for " + settings.ENVIRONMENT + " environment")

# Kafka settings
topics_to_subscribe = settings.KAFKA_TOPICS.split(",")
bootstrap_servers = settings.KAFKA_INSTANCE.split(",")
logger.info(f"Bootstrapping from servers {bootstrap_servers}")
logger.info(f"Subscribing to topics {topics_to_subscribe}")

# loop = asyncio.get_event_loop()

# consumer = AIOKafkaConsumer(
#     *topics_to_subscribe, loop=loop,
#     bootstrap_servers=bootstrap_servers
# )

# logger.info(f"Consumer creation succeeded")

# # Async Kafka routine to consume
# async def consume():
#     while True:
#         logger.info(f"Consuming messages now")
#         async for msg in consumer:
#             payload = {
#                 "topic": msg["topic"],
#                 "partition": msg["partition"],
#                 "offset": msg["offset"],
#                 "key": msg["key"],
#                 "value": msg["value"],
#                 "timestamp": msg["timestamp"]
#             }
#             logger.info("Received ", str(payload))

# Connecting to the datatabase and running kafka
@app.on_event("startup")
async def startup():
    logger.info("Application startup")
    await db.connect_to_database(path=settings.DB_URI, db_name=settings.DB_NAME)
    # await consumer.start()
    # await consume()

# Disconnecting from the database
@app.on_event("shutdown")
async def shutdown():
    logger.info("Discconnecting to the database")
    await db.close_database_connection()
    # await consumer.stop()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)