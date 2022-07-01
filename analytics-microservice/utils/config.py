import os
import secrets

from functools import lru_cache

from pydantic import BaseSettings


def database_uri():
    """
    DB connection details
    """
    # DB_USER = os.getenv("POSTGRES_USERNAME", "admin")
    # DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "ds&bd2021-2022")
    DB_NAME = os.getenv("CLICKHOUSE_DB", "default")
    DB_HOST = os.getenv("CLICKHOUSE_HOST", "clickhouse")
    DB_PORT = os.getenv("CLICKHOUSE_PORT", "8123")

    CLIENT_SETUP = (
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return CLIENT_SETUP


class Settings(BaseSettings):
    """
    App config settings
    """

    PROJECT_NAME: str = os.getenv("PROJECT_NAME3", "Analytics-Microservice")
    VERSION: str = "1.0"
    DESCRIPTION: str = "App to get analytical reports on IoT devices activity"
    SECRET_KET: str = secrets.token_urlsafe(32)
    DEBUG: bool = bool(os.getenv("DEBUG", "False"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    DB_NAME: str = os.getenv("MONGO_DB", "conf")
    DB_URI = database_uri()
    KAFKA_HOST: str = os.getenv("KAFKA_HOST", "kafka")
    KAFKA_PORT: str = os.getenv("KAFKA_PORT", "9092")
    KAFKA_PORT_EXTERNAL: str = os.getenv("KAFKA_PORT_EXTERNAL", "9093")
    KAFKA_TOPICS: str = os.getenv("RECORDING_MICROSERVICE_KAFKA_TOPICS", "measure_recordings,device_commands")
    KAFKA_INSTANCE = f"{KAFKA_HOST}:{KAFKA_PORT}"
    KAFKA_INSTANCE_LOCALHOST = f"localhost:{KAFKA_PORT_EXTERNAL}"
    KAFKA_CONSUMER_GROUP = "analytics"
    KAFKA_RECORDING_TOPIC = "measure_recordings"
    MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "broker.hivemq.com")
    MQTT_BROKER_PORT = os.getenv("MQTT_BROKER_PORT", 1883)
    MQTT_TOPIC_PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "rmp/dsbd202122/")

    class Config:
        case_sensitive = True


@lru_cache
def get_config():
    return Settings()
