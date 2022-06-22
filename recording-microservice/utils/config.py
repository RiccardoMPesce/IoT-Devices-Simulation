import os
import secrets

from functools import lru_cache

from pydantic import BaseSettings


def database_uri():
    """
    DB connection details
    """
    DB_USER = os.getenv("POSTGRES_USERNAME", "admin")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "ds&bd2021-2022")
    DB_NAME = os.getenv("POSTGRES_DB", "recordings")

    MONGODB_CLIENT_SETUP = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@postgres:5432/{DB_NAME}"
    )

    return MONGODB_CLIENT_SETUP


class Settings(BaseSettings):
    """
    App config settings
    """

    PROJECT_NAME: str = "Monitoring-Management-Microservice"
    VERSION: str = "1.0"
    DESCRIPTION: str = "Simple app to monitor and manage IoT remote devices"
    SECRET_KET: str = secrets.token_urlsafe(32)
    DEBUG: bool = bool(os.getenv("DEBUG", "False"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    DB_NAME: str = os.getenv("MONGO_DB", "conf")
    DB_URI = database_uri()
    KAFKA_HOST: str = os.getenv("KAFKA_HOST", "kafka")
    KAFKA_PORT: str = os.getenv("KAFKA_PORT", "9092")
    KAFKA_PORT_EXTERNAL: str = os.getenv("KAFKA_PORT_EXTERNAL", "9093")
    KAFKA_TOPICS: str = os.getenv("KAFKA_TOPICS", "measure_recordings")
    KAFKA_INSTANCE = f"{KAFKA_HOST}:{KAFKA_PORT}"
    KAFKA_INSTANCE_LOCALHOST = f"localhost:{KAFKA_PORT_EXTERNAL}"
    KAFKA_CONSUMER_GROUP = PROJECT_NAME.lower().replace("-microservice", "")
    MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "broker.hivemq.com")
    MQTT_TOPIC_PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "rmp/dsbd202122/")

    class Config:
        case_sensitive = True


@lru_cache
def get_config():
    return Settings()
