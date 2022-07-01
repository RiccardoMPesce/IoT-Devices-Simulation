import os
import secrets

from functools import lru_cache

from pydantic import BaseSettings


def database_uri():
    """
    DB connection details
    """
    POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "admin")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "ds&bd2021-2022")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "recordings")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    DB_CLIENT_SETUP = (
        f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    return DB_CLIENT_SETUP


class Settings(BaseSettings):
    """
    App config settings
    """

    PROJECT_NAME: str = os.getenv("PROJECT_NAME2", "Recording-Microservice")
    VERSION: str = "1.0"
    DESCRIPTION: str = "Simple app to record IoT sensors measures"
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
    KAFKA_CONSUMER_GROUP = PROJECT_NAME.lower().replace("-microservice", "")
    MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "broker.hivemq.com")
    MQTT_BROKER_PORT = os.getenv("MQTT_BROKER_PORT", 1883)
    MQTT_TOPIC_PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "rmp/dsbd202122/")

    class Config:
        case_sensitive = True


@lru_cache
def get_config():
    return Settings()
