import databases
import ormar
import sqlalchemy

from utils.config import get_config

from datetime import datetime

settings = get_config()

class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)