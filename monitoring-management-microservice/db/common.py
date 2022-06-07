from db.database_manager import DatabaseManager
from db.mongo_manager import MongoManager

db = MongoManager()

async def get_database() -> DatabaseManager:
    return db
