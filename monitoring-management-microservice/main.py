# Used to run the server
import uvicorn

from fastapi import FastAPI

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

@fast_mqtt.on_connect()
def mqtt_connect(client, flags, rc, properties):
    # Later for subscription
    logger.info("Connected: ", str(client), str(flags), str(rc), str(properties))

@fast_mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print(str(client), " eceived message: ", str(topic), str(payload.decode()), str(qos), str(properties))
    return 0

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

# Including routes
app.include_router(endpoint)

settings = get_config()

logger = logger_config(__name__)

# Add Prometheus
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

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

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    reload = True
    num_workers = 2
    
    logger.info(f"Running app {settings.PROJECT_NAME} on {host}:{port}")
    if reload:
        logger.info("Reload is enabled")
    else:
        logger.info("Reload is disabled")
    logger.info(f"Number of workers: {num_workers}")

    uvicorn.run("main:app", host=host, port=port, reload=reload, workers=num_workers)
