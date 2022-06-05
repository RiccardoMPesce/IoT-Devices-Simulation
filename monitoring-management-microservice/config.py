import os
import secrets
from functools import lru_cache

from pydantic import BaseSettings


def database_uri():
    """
    DB connection details
    """
    DB_HOST = os.getenv("MONGO_HOST", "localhost")
    DB_PORT = os.getenv("MONGO_PORT", "27017")
    DB_NAME = os.getenv("MONGO_DB", "conf")
    DB_USERNAME = os.getenv("MONGO_USER")
    DB_PASSWORD = os.getenv("MONGO_PASSWORD")

    MONGODB_CLIENT_SETUP = (
        f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return MONGODB_CLIENT_SETUP


class Settings(BaseSettings):
    """
    App config settings
    """

    PROJECT_NAME: str
    VERSION: str
    DESCRIPTION: str
    SECRET_KET: str = secrets.token_urlsafe(32)
    DEBUG: bool = bool(os.getenv("DEBUG", "False"))
    ENVIRONMENT: str
    DB_URI = database_uri()

    class Config:
        case_sensitive = True


@lru_cache
def get_config():
    return Settings()
