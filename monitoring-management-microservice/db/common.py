from db.database_manager import DeviceDatabaseManager, MeasureDatabaseManager
from db.mongo_manager import DeviceMongoManager, MeasureMongoManager

device_db = DeviceMongoManager()
measure_db = MeasureMongoManager()


async def get_device_database() -> DeviceDatabaseManager:
    return device_db

async def get_measure_database() -> MeasureDatabaseManager:
    return measure_db