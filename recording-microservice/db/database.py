import databases
import ormar
import sqlalchemy

from datetime import datetime
from typing import Union

from utils.config import get_config

settings = get_config()

database = databases.Database(settings.DB_URI)
metadata = sqlalchemy.MetaData()

class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database

class Record(ormar.Model):
    class Meta(BaseMeta):
        # tablename = "record"
        pass

    recording_id: int = ormar.Integer(primary_key=True, autoincrement=True)
    device_id: str = ormar.UUID(nullable=False)
    measure: str = ormar.String(max_length=256, nullable=False)
    is_device_healthy: bool = ormar.Boolean(default=True, nullable=False)
    timestamp: datetime = ormar.DateTime(default=datetime.utcnow, nullable=False)
    value: float = ormar.Float(nullable=False)

engine = sqlalchemy.create_engine(settings.DB_URI)
metadata.drop_all(engine)
metadata.create_all(engine)
