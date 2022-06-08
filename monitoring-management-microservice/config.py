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
    DB_PASSWORD = os.getenv("MONGO_PASSWORD", "ds&bd2021-2022")

    MONGODB_CLIENT_SETUP = (
        f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource={DB_USERNAME}"
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
    DB_URI = database_uri()

    class Config:
        case_sensitive = True


@lru_cache
def get_config():
    return Settings()
