import uvicorn
import asyncio

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

# Used to add Prometheus support
from starlette_exporter import PrometheusMiddleware, handle_metrics

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

# Init MQTT
fast_mqtt.init_app(app)

# Including routes
app.include_router(endpoint)

# Add Prometheus
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

logger.info("API launched for " + settings.ENVIRONMENT + " environment")

# Startup event routine
@app.on_event("startup")
async def startup():
    logger.info("Application startup")
    await db.connect_to_database(path=settings.DB_URI, db_name=settings.DB_NAME)
    asyncio.create_task(kafka_init())
    asyncio.create_task(consume())

# Shutdown event routine
@app.on_event("shutdown")
async def shutdown():
    logger.info("Application shutdown")
    await db.close_database_connection()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)