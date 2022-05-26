from typing import Optional, Union
from datetime import datetime
from uuid import uuid4

from common import *
from models.device_schema import DeviceSchema

from repository.device_repository import *

async def retrieve_devices():
    pass

async def add_device_service(measure: str, publish_qos: int, status: Union[bool, int, str, None], decading_factor: Optional[float] = None):
    update_datetime = datetime.utcnow().timestamp()
    device_id = str(uuid4())
    device_data = {
        "device_id": device_id,
        "measure": measure,
        "publish_qos": publish_qos,
        "status": status,
        "update_datetime": update_datetime
    }
    return await add_device_repository(device_data)


async def retrieve_device_service():
    pass

async def update_device_service():
    pass

async def delete_device_service():
    pass