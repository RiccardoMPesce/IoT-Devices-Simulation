import os
import secrets

from functools import lru_cache

from pydantic import BaseSettings


def database_uri():
    """
    DB connection details
    """
    DB_HOST = os.getenv("MONGO_HOST", "mongodb")
    DB_PORT = os.getenv("MONGO_PORT", "27017")
    DB_NAME = os.getenv("MONGO_DB", "conf")
    DB_USERNAME = os.getenv("MONGO_USER", "admin")
    DB_PASSWORD = os.getenv("MONGO_PASSWORD")

    MONGODB_CLIENT_SETUP = (
        f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource={DB_USERNAME}"
    )

    return MONGODB_CLIENT_SETUP


class Settings(BaseSettings):
    """
    App config settings
    """

    PROJECT_NAME: str = os.getenv("PROJECT_NAME1", "Monitoring-Management-Microservice")
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
    MQTT_BROKER_PORT = os.getenv("MQTT_BROKER_PORT", 1883)
    MQTT_TOPIC_PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "rmp/dsbd202122/")
    PROMETHEUS_HOST = os.getenv("PROMETHEUS_HOST", "prometheus")
    PROMETHEUS_PORT = os.getenv("PROMETHEUS_PORT", "9090")
    PUSHGATEWAY_HOST = os.getenv("PUSHGATEWAY_HOST", "pushgateway")
    PUSHGATEWAY_PORT = os.getenv("PUSHGATEWAY_PORT", "9091")
    PROMETHEUS_INSTANCE = f"{PROMETHEUS_HOST}:{PROMETHEUS_PORT}"
    PUSHGATEWAY_INSTANCE = f"{PUSHGATEWAY_HOST}:{PUSHGATEWAY_PORT}"

    class Config:
        case_sensitive = True


@lru_cache
def get_config():
    return Settings()
