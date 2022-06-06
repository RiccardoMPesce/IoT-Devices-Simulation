# Used to run the server
import uvicorn

from fastapi import FastAPI

# Used to add Prometheus support
from starlette_exporter import PrometheusMiddleware, handle_metrics

from config import get_config
from db.common import get_device_database, get_measure_database
from api.endpoint import endpoint
from utils.logger import logger_config

from datetime import datetime

app = FastAPI(title="Monitoring & Management Microservice")

app.include_router(endpoint)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
