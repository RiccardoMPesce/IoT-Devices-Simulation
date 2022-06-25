from aiochclient import ChClient
from aiohttp import ClientSession

from utils.logger import logger_config

logger = logger_config(__name__)

async def test_clickhouse():
    async with ClientSession() as s:
        client = ChClient(
            s, 
            url="clickhouse://clickhouse:8123",
            database="default"
        )
        logger.info(f"Client is alive -> {await client.is_alive()}")
        assert await client.is_alive()
