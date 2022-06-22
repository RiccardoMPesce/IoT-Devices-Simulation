import databases
import ormar
import sqlalchemy

from utils.config import get_config

from datetime import datetime

settings = get_config()

database = databases.Database(settings.DB_URI)
metadata = sqlalchemy.MetaData()
class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database

engine = sqlalchemy.create_engine(settings.DB_URI)
metadata.create_all(engine)