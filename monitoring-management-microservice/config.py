import os
import secrets
from functools import lru_cache

from pydantic import BaseSettings


def database_uri():
    """
    DB connection details
    """
    db_host = os.getenv("MONGO_HOST", "mongodb")
    db_port = os.getenv("MONGO_PORT", "27017")
    db_name = os.getenv("MONGO_DB", "conf")
    db_username = os.getenv("MONGO_USER", "admin")
    db_password = os.getenv("MONGO_PASSWORD")

    mongodb_client_setup = (
        f"mongodb://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    return mongodb_client_setup


class Settings(BaseSettings):
    """
    App config settings
    """

    project_name: str
    version: str
    description: str
    secret_ket: str = secrets.token_urlsafe(32)
    debug: bool = bool(os.getenv("DEBUG", "False"))
    environment: str
    db_uri = database_uri()

    class Config:
        case_sensitive = True


@lru_cache
def get_config():
    return Settings()
