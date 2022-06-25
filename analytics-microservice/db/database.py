from aiochclient import ChClient
from aiohttp import ClientSession

from utils.logger import logger_config
from utils.config import get_config

logger = logger_config(__name__)

settings = get_config()


async def test_ch():
    async with ClientSession() as s:
        client = ChClient(
            s, 
            url=settings.DB_URI,
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
                                value                 Float64
                            )
                            ENGINE = Kafka 
                            SETTINGS
                                kafka_broker_list = '{settings.KAFKA_INSTANCE}',
                                kafka_topic_list = '{settings.KAFKA_RECORDING_TOPIC}',
                                kafka_group_name = '{settings.KAFKA_CONSUMER_GROUP}',
                                kafka_format = 'JSONEachRow'
                                ;
                        """


CH_QUERY_DWH_TABLE =    f"""
                            CREATE TABLE IF NOT EXISTS dwh.fact_recording
                            (
                                record_id             Int32,
                                device_id             UUID,
                                measure               String,
                                is_device_healthy     Bool,
                                timestamp             DateTime,
                                value                 Float64
                            )
                            ENGINE = MergeTree 
                            ORDER BY (measure, timestamp)
                            PARTITION_BY timestamp
                            ;
                        """


CH_QUERY_MV_DWH_TABLE = f"""
                            CREATE MATERIALIZED VIEW stage.mv_fact_recording
                            TO dwh.fact_recording
                            AS SELECT *
                            FROM stage.kafka_fact_recording
                            ;
                        """


async def ch_init():
    async with ClientSession() as s:
        init_client = ChClient(
            s, 
            url=settings.DB_URI,
            compress_response=True
        )
        await init_client.execute("CREATE DATABASE IF NOT EXISTS stage;")
        logger.info("Database \"stage\" created/already present")
        await init_client.execute("CREATE DATABASE IF NOT EXISTS dwh;")
        logger.info("Database \"dwh\" created/already present")
        await init_client.execute("CREATE DATABASE IF NOT EXISTS marts;")
        logger.info("Database \"marts\" created/already present")

        result = await init_client.execute(CH_QUERY_KAFKA_TABLE)
        logger.info(f"Created stage.kafka_fact_recording table with query: {CH_QUERY_KAFKA_TABLE}")
