from aiochclient import ChClient
from aiohttp import ClientSession

from utils.logger import logger_config

logger = logger_config(__name__)

async def test_ch():
    async with ClientSession() as s:
        client = ChClient(
            s, 
            url="clickhouse://clickhouse:8123",
            database="default"
        )
        logger.info(f"Client is alive -> {await client.is_alive()}")
        assert await client.is_alive()

CH_QUERY_KAFKA_TABLE =  f"""
                            CREATE TABLE IF NOT EXISTS stage.kafka_fact_recording
                            (
                                record_id             Int32,
                                device_id             UUID,
                                measure               String,
                                is_device_healthy     Bool,
                                timestamp             DateTime,
                                value                 Decimal64
                            )
                            ENGINE = Kafka("localhost:9292", "payments_topic", "payments_group1, "JSONEachRow");
                        """

async def ch_init():
    async with ClientSession() as s:
        init_client = ChClient(
            s, 
            url="clickhouse://clickhouse:8123"
        )

        await init_client.execute("CREATE DATABASE IF NOT EXISTS stage;")
        logger.info("Database \"stage\" created/already present")
        await init_client.execute("CREATE DATABASE IF NOT EXISTS dwh;")
        logger.info("Database \"dwh\" created/already present")
        await init_client.execute("CREATE DATABASE IF NOT EXISTS marts;")
        logger.info("Database \"marts\" created/already present")
