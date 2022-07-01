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
                                record_id             UInt32,
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
                                record_id             UInt32,
                                device_id             String,
                                measure               String,
                                health                UInt8,
                                timestamp             DateTime,
                                update_epoch          UInt32,    
                                measure_value         Float64
                            )
                            ENGINE = MergeTree 
                            ORDER BY (record_id, device_id, measure, toYYYYMMDD(timestamp))
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
                                device_id             String,
                                measure               String,
                                health                AggregateFunction(argMax, UInt8, UInt32),
                                timestamp             AggregateFunction(argMax, DateTime, UInt32),
                                update_epoch          AggregateFunction(argMax, UInt32, UInt32),
                                measure_value         AggregateFunction(argMax, Float64, UInt32)
                            )
                            ENGINE = SummingMergeTree 
                            ORDER BY (device_id, measure)
                            ;
                        """


CH_QUERY_MV_MARTS_TABLE = f"""
                            CREATE MATERIALIZED VIEW IF NOT EXISTS marts.mv_fact_recording
                            TO marts._fact_recording
                            AS SELECT device_id,
                                      measure,
                                      argMaxState(health, fr.update_epoch)            AS health,
                                      argMaxState(timestamp, fr.update_epoch)         AS timestamp,
                                      argMaxState(update_epoch, fr.update_epoch)      AS update_epoch,
                                      argMaxState(measure_value, fr.update_epoch)     AS measure_value
                            FROM dwh.fact_recording AS fr
                            GROUP BY device_id,
                                     measure  
                            ;
                        """


CH_QUERY_MARTS_VIEW =   f"""
                            CREATE VIEW IF NOT EXISTS marts.fact_recording
                            TO marts._fact_recording
                            AS SELECT device_id,
                                      measure,
                                      argMaxMerge(health)            AS health,
                                      argMaxMerge(timestamp)         AS timestamp,
                                      argMaxMerge(update_epoch)      AS update_epoch,
                                      argMaxMerge(measure_value)     AS measure_value
                            FROM marts._fact_recording
                            GROUP BY device_id,
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

        # for table_name, table_query in tables_to_create.items():
        #     await init_client.execute(f"DROP TABLE IF EXISTS {table_name};")
        
        for table_name, table_query in tables_to_create.items():
            await init_client.execute(table_query)
            logger.info(f"Created table {table_name} with query:\n{table_query}")


async def stats_by_device(device_id: str) -> dict:
    async with ClientSession() as s:
        client = ChClient(
            s, 
            url=settings.DB_URI,
            compress_response=True
        )

        dwh_query = f"""
                    SELECT * 
                    FROM dwh.fact_recording 
                    WHERE device_id = '{device_id}'
                """
        
        marts_query = f"""
                    SELECT * 
                    FROM marts.fact_recording 
                    WHERE device_id = '{device_id}'
                """

        device_stats = {}
        
        measure_obs = []
        measure_health = []

        logger.info(f"Using query:\n{dwh_query}")
        async for row in client.iterate(dwh_query):
            measure_obs += [row["measure_value"]] 
            measure_health += [row["health"]]

        device_stats["average"] = round(sum(measure_obs) / len(measure_obs), 2)
        device_stats["standard_deviation"] = round((sum([
            (obs - device_stats["average"]) ** 2 for obs in measure_obs
        ])) ** 0.5, 2)
        device_stats["average_health_uptime_fraction"] = sum(measure_health) / len(measure_health)

        logger.info(f"Using query:\n{marts_query}")
        
        row = await client.fetchone(marts_query)

        device_stats["last_update"] = row["timestamp"]
        device_stats["last_value"] = row["measure_value"]
        device_stats["max_value"] = max(measure_obs)
        device_stats["min_value"] = min(measure_obs)
        device_stats["is_healthy"] = row["health"]
        device_stats["measure"] = row["measure"]
        device_stats["device_id"] = row["device_id"]
        device_stats["number_of_observations"] = len(measure_obs)

        return device_stats

    

async def stats_by_measure(measure: str):
    async with ClientSession() as s:
        client = ChClient(
            s, 
            url=settings.DB_URI,
            compress_response=True
        )

        dwh_query = f"""
                    SELECT * 
                    FROM dwh.fact_recording 
                    WHERE measure = '{measure}'
                """
        
        marts_query = f"""
                    SELECT * 
                    FROM marts.fact_recording 
                    WHERE measure = '{measure}'
                """

        measure_stats = {}
        
        measure_obs = []
        measure_health = []
        
        measure_devices = set()

        logger.info(f"Using query:\n{dwh_query}")
        async for row in client.iterate(dwh_query):
            measure_obs += [row["measure_value"]] 
            measure_health += [row["health"]]
            measure_devices.add(row["device_id"])

        measure_stats["average"] = round(sum(measure_obs) / len(measure_obs), 2)
        measure_stats["standard_deviation"] = round((sum([
            (obs - measure_stats["average"]) ** 2 for obs in measure_obs
        ])) ** 0.5, 2)
        measure_stats["max_value"] = max(measure_obs)
        measure_stats["min_value"] = min(measure_obs)

        logger.info(f"Using query:\n{marts_query}")
        
        row = await client.fetchone(marts_query)

        measure_stats["last_update"] = row["timestamp"]
        measure_stats["last_value"] = row["measure_value"]
        measure_stats["last_device"] = row["device_id"]
        measure_stats["measure"] = row["measure"]
        measure_stats["devices"] = list(measure_devices)

        return measure_stats

async def last_device_state(device_id: str) -> dict:
    async with ClientSession() as s:
        client = ChClient(
            s, 
            url=settings.DB_URI,
            compress_response=True
        )
        
        marts_query = f"""
                    SELECT * 
                    FROM marts.fact_recording 
                    WHERE device_id = '{device_id}'
                """

        row = await client.fetchone(marts_query)

        return dict(row)

async def last_measure_state(measure: str) -> dict:
    async with ClientSession() as s:
        client = ChClient(
            s, 
            url=settings.DB_URI,
            compress_response=True
        )
        
        marts_query = f"""
                    SELECT * 
                    FROM marts.fact_recording 
                    WHERE measure = '{measure}'
                """

        row = await client.fetchone(marts_query)

        return dict(row)


async def remove_entry(recording_id: int):
    async with ClientSession() as s:
        client = ChClient(
            s, 
            url=settings.DB_URI,
            compress_response=True
        )
        
        remove_query = f"ALTER TABLE dwh.fact_recording DELETE WHERE record_id = {recording_id};"

        logger.info(f"Removing recording {recording_id} with query: {remove_query}")

        result = await client.execute(remove_query)

        logger.info(f"Result {result}")