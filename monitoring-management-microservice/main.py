# Used to run the server
import uvicorn

from fastapi import FastAPI

# Used to add Prometheus support
from starlette_exporter import PrometheusMiddleware, handle_metrics

from config import get_config
from db.common import get_database, db
from api.endpoint import endpoint
from utils.logger import logger_config
from utils.kafka_consumer import consume

from datetime import datetime

from api.simulation_api import fast_mqtt

settings = get_config()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs"
)

fast_mqtt.init_app(app)

app.include_router(endpoint)

settings = get_config()

logger = logger_config(__name__)

# Add Prometheus
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

logger.info("API launched for " + settings.ENVIRONMENT + " environment")

# Connecting to the datatabase
@app.on_event("startup")
async def startup():
    logger.info("Connecting to the database")
    await db.connect_to_database(path=settings.DB_URI, db_name=settings.DB_NAME)
    await consume()

# Disconnecting from the database
@app.on_event("shutdown")
async def startup():
    logger.info("Connecting to the database")
    await db.close_database_connection()
    await consumer.stop()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
