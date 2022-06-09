# Used to run the server
import uvicorn

from fastapi import FastAPI

# Used to add Prometheus support
from starlette_exporter import PrometheusMiddleware, handle_metrics

from config import get_config
from db.common import get_database, db
from api.endpoint import endpoint
from utils.logger import logger_config

# MQTT
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig

from datetime import datetime

settings = get_config()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs"
)

mqtt_config = MQTTConfig()

fast_mqtt = FastMQTT(config=mqtt_config)

fast_mqtt.init_app(app)

app.include_router(endpoint)

settings = get_config()

logger = logger_config(__name__)

# MQTT settings
@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt")
    print("Connected: ", client, flags, rc, properties)

# Add Prometheus
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

logger.info("API launched for " + settings.ENVIRONMENT + " environment")

# Connecting to the datatabase
@app.on_event("startup")
async def startup():
    logger.info("Connecting to the database")
    await db.connect_to_database(path=settings.DB_URI, db_name=settings.DB_NAME)

# Disconnecting from the database
@app.on_event("shutdown")
async def startup():
    logger.info("Connecting to the database")
    await db.close_database_connection()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
