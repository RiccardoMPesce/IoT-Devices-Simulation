from fastapi import FastAPI

# CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

# Used to add Prometheus support
from starlette_exporter import PrometheusMiddleware, handle_metrics

from config import get_config
from db.common import db
from api.endpoint import endpoint
from utils.logger import logger_config

from aiokafka import AIOKafkaConsumer

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

# Async Kafka routine to consume
async def consume():
    topics_to_subscribe = settings.KAFKA_TOPICS.split(",")
    bootstrap_servers = settings.KAFKA_INSTANCE.split(",")
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

# Connecting to the datatabase and running kafka
@app.on_event("startup")
async def startup():
    logger.info("Connecting to the database")
    await db.connect_to_database(path=settings.DB_URI, db_name=settings.DB_NAME)
    # await consume()

# Disconnecting from the database
@app.on_event("shutdown")
async def shutdown():
    logger.info("Discconnecting to the database")
    await db.close_database_connection()

