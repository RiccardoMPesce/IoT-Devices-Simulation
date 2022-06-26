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
                                device_id             String,
                                measure               String,
                                health                UInt8,
                                timestamp             UInt32,
                                measure_value         Float64
                            )
                            ENGINE = Kafka 
                            SETTINGS
                                kafka_broker_list = '{settings.KAFKA_INSTANCE}',
                                kafka_topic_list = '{settings.KAFKA_RECORDING_TOPIC}',
                                kafka_group_name = '{settings.KAFKA_CONSUMER_GROUP}',
                                kafka_format = 'JSONEachRow',
                                kafka_row_delimiter = '\n',
                                kafka_num_consumers = 1,
                                kafka_skip_broken_messages = 1
                                ;
                        """


CH_QUERY_DWH_TABLE =    f"""
                            CREATE TABLE IF NOT EXISTS dwh.fact_recording
                            (
                                record_id             Int32,
                                device_id             String,
                                measure               String,
                                health                UInt8,
                                timestamp             DateTime,
                                update_epoch          UInt32,    
                                measure_value         Float64
                            )
                            ENGINE = MergeTree 
                            ORDER BY (record_id, measure, toYYYYMMDD(timestamp))
                            ;
                        """


CH_QUERY_MV_DWH_TABLE = f"""
                            CREATE MATERIALIZED VIEW IF NOT EXISTS dwh.mv_fact_recording
                            TO dwh.fact_recording
                            AS SELECT record_id,
                                      device_id,
                                      measure,
                                      health,
                                      toDateTime(timestamp)  AS timestamp,
                                      toUnixTimestamp(now()) AS update_epoch,
                                      measure_value  
                            FROM stage.kafka_fact_recording
                            GROUP BY record_id, device_id, measure, health, timestamp, measure_value
                            ;
                        """


CH_QUERY_MARTS_TABLE =  f"""
                            CREATE TABLE IF NOT EXISTS marts._fact_recording
                            (
                                record_id             Int32,
                                device_id             String,
                                measure               String,
                                health                AggregateFunction(argMax, UInt8, UInt32),
                                timestamp             AggregateFunction(argMax, DateTime, UInt32),
                                update_epoch          AggregateFunction(argMax, UInt32, UInt32),
                                measure_value         AggregateFunction(argMax, Float64, UInt32)
                            )
                            ENGINE = SummingMergeTree 
                            ORDER BY (record_id, device_id, measure)
                            ;
                        """


CH_QUERY_MV_MARTS_TABLE = f"""
                            CREATE MATERIALIZED VIEW IF NOT EXISTS marts.mv_fact_recording
                            TO marts._fact_recording
                            AS SELECT record_id,
                                      device_id,
                                      measure,
                                      argMaxState(health, fr.update_epoch)            AS health,
                                      argMaxState(timestamp, fr.update_epoch)         AS timestamp,
                                      argMaxState(update_epoch, fr.update_epoch)      AS update_epoch,
                                      argMaxState(measure_value, fr.update_epoch)     AS measure_value
                            FROM dwh.fact_recording AS fr
                            GROUP BY record_id,
                                     device_id,
                                     measure  
                            ;
                        """


CH_QUERY_MARTS_VIEW =   f"""
                            CREATE VIEW IF NOT EXISTS marts.fact_recording
                            TO marts._fact_recording
                            AS SELECT record_id,
                                      device_id,
                                      measure,
                                      argMaxMerge(health)            AS health,
                                      argMaxMerge(timestamp)         AS timestamp,
                                      argMaxMerge(update_epoch)      AS update_epoch,
                                      argMaxMerge(measure_value)     AS measure_value
                            FROM marts._fact_recording
                            GROUP BY record_id,
                                     device_id,
                                     measure  
                            ;
                        """


tables_to_create = {
    "stage.kafka_fact_recording": CH_QUERY_KAFKA_TABLE,
    "dwh.fact_recording": CH_QUERY_DWH_TABLE,
    "dwh.mv_fact_recording": CH_QUERY_MV_DWH_TABLE,
    "marts._fact_recording": CH_QUERY_MARTS_TABLE,
    "marts.mv_fact_recording": CH_QUERY_MV_MARTS_TABLE,
    "marts.fact_recording": CH_QUERY_MARTS_VIEW
}


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

        for table_name, table_query in tables_to_create.items():
            await init_client.execute(f"DROP TABLE IF EXISTS {table_name};")
        
        for table_name, table_query in tables_to_create.items():
            await init_client.execute(table_query)
            logger.info(f"Created table {table_name} with query:\n{table_query}")
