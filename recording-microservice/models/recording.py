import ormar

from typing import Union

from db.database import BaseMeta

from datetime import datetime

class Record(ormar.Model):
    class Meta(BaseMeta):
        tablename = "record"

    recording_id: str = ormar.Integer(primary_key=True)
    device_id: str = ormar.String(max_length=256, foreign_key=True, unique=True, nullable=False)
    measure: str = ormar.String(max_length=256, unique=True, nullable=False)
    is_device_healthy: bool = ormar.Boolean(default=True, nullable=False)
    timestamp: datetime = ormar.DateTime(nullable=False)
    value: Union[int, str, bool, float]

class FloatRecord(ormar.Model):
    class Meta(BaseMeta):
        tablename = "float_record"

    recording_id: str = ormar.Integer(primary_key=True)
    device_id: str = ormar.String(max_length=256, foreign_key=True, unique=True, nullable=False)
    measure: str = ormar.String(max_length=256, unique=True, nullable=False)
    is_device_healthy: bool = ormar.Boolean(default=True, nullable=False)
    timestamp: datetime = ormar.DateTime(nullable=False)
    value: float = ormar.Float(nullable=False)

class IntRecord(ormar.Model):
    class Meta(BaseMeta):
        tablename = "int_record"

    recording_id: int = ormar.Integer(primary_key=True)
    device_id: str = ormar.String(max_length=256, foreign_key=True, unique=True, nullable=False)
    measure: str = ormar.String(max_length=256, unique=True, nullable=False)
    is_device_healthy: bool = ormar.Boolean(default=True, nullable=False)
    timestamp: datetime = ormar.DateTime(nullable=False)
    value: int = ormar.Integer(nullable=False)

class StringRecord(ormar.Model):
    class Meta(BaseMeta):
        tablename = "string_record"

    recording_id: int = ormar.Integer(primary_key=True)
    device_id: str = ormar.String(max_length=256, foreign_key=True, unique=True, nullable=False)
    measure: str = ormar.String(max_length=256, unique=True, nullable=False)
    is_device_healthy: bool = ormar.Boolean(default=True, nullable=False)
    timestamp: datetime = ormar.DateTime(nullable=False)
    value: str = ormar.String(max_length=16, nullable=False)

class BooleanRecord(ormar.Model):
    class Meta(BaseMeta):
        tablename = "boolean_record"

    recording_id: int = ormar.Integer(primary_key=True)
    device_id: str = ormar.String(max_length=256, foreign_key=True, unique=True, nullable=False)
    measure: str = ormar.String(max_length=256, unique=True, nullable=False)
    is_device_healthy: bool = ormar.Boolean(default=True, nullable=False)
    timestamp: datetime = ormar.DateTime(nullable=False)
    value: bool = ormar.Boolean(nullable=False)