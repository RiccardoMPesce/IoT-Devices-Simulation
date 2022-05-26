from typing import Optional, Union
from datetime import datetime
from uuid import uuid4

from common import *
from models.device_schema import DeviceSchema

from repository.device_repository import *

async def retrieve_devices():
    pass

async def add_device(measure: str, publish_qos: int, status: Union[bool, int, str, None], decading_factor: Optional[float] = None):
    added_timestamp = datetime.utcnow().timestamp()
    device_id = str(uuid4())
    return await add_device(measure, publish_qos, status, decading_factor)


async def retrieve_device():
    pass

async def update_device():
    pass

async def delete_device():
    pass