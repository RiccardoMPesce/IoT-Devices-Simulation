import databases
import ormar
import sqlalchemy

from utils.config import get_config

from datetime import datetime

settings = get_config()

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class FloatRecord(ormar.Model):
    class Meta(BaseMeta):
        tablename = "float_record"

    recording_id: str = ormar.Integer(primary_key=True)
    device_id: str = ormar.String(foreign_key=True, unique=True, nullable=False)
    measure: str = ormar.String(unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)
    is_device_healthy: bool = ormar.Boolean(default=True, nullable=False)
    timestamp: datetime = ormar.DateTime(nullable=False)
    value: float = ormar.Float(nullable=False)


class IntRecord(ormar.Model):
    class Meta(BaseMeta):
        tablename = "int_record"

    recording_id: int = ormar.Integer(primary_key=True)
    device_id: str = ormar.String(foreign_key=True, unique=True, nullable=False)
    measure: str = ormar.String(unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)
    is_device_healthy: bool = ormar.Boolean(default=True, nullable=False)
    timestamp: datetime = ormar.DateTime(nullable=False)
    value: int = ormar.Integer(nullable=False)


class StringRecord(ormar.Model):
    class Meta(BaseMeta):
        tablename = "string_record"

    recording_id: int = ormar.Integer(primary_key=True)
    device_id: str = ormar.String(foreign_key=True, unique=True, nullable=False)
    measure: str = ormar.String(unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)
    is_device_healthy: bool = ormar.Boolean(default=True, nullable=False)
    timestamp: datetime = ormar.DateTime(nullable=False)
    value: str = ormar.String(nullable=False)


class BooleanRecord(ormar.Model):
    class Meta(BaseMeta):
        tablename = "boolean_record"

    recording_id: int = ormar.Integer(primary_key=True)
    device_id: str = ormar.String(foreign_key=True, unique=True, nullable=False)
    measure: str = ormar.String(unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)
    is_device_healthy: bool = ormar.Boolean(default=True, nullable=False)
    timestamp: datetime = ormar.DateTime(nullable=False)
    value: bool = ormar.Boolean(nullable=False)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)