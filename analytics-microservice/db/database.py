from clickhouse_driver import Client

from utils.logger import logger_config

logger = logger_config(__name__)

async def test_clickhouse():
    client = Client(
        host="clickhouse",
        port="9000",
        database="default"
    )

    logger.info(f"Clickhouse {client}")
    
    try:
        client.execute("SELECT * FROM default.test;")
    except Exception as e:
        logger.info(f"Exception occurred")
        logger.info(e)