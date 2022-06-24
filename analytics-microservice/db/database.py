from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DDL

from utils.logger import logger_config

logger = logger_config(__name__)

async def test_clickhouse():
    conn_str = "clickhouse://default:@clickhouse:8123/default"

    engine = create_engine(conn_str)
    session = sessionmaker(bind=engine)()

    database = "test"

    engine.execute(DDL(f"CREATE DATABASE IF NOT EXISTS {database}"))

    logger.info(f"{session}")
    