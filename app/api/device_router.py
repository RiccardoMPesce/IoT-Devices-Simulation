from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from typing import Optional, Union
from datetime import datetime
from uuid import uuid4

from models.device_schema import DeviceSchema
from models.response_schema import ResponseModel

from common import status_to_bool_dict

from database.device_crud import (
    retrieve_devices,
    retrieve_device, 
    add_device,
    update_device,
    delete_device
)

router = APIRouter()

@router.post("/", response_description="Device data added into the database")
async def add_device_data(measure: str, publish_qos: int, status: Union[bool, int, float, str]):
    device = {
        "device_id": str(uuid4()),
        "measure": measure,
        "publish_qos": publish_qos,
        "status": status_to_bool_dict.get(status, False),
        "update_datetime": datetime.utcnow().timestamp()
    }
    added_device = await add_device(jsonable_encoder(device))
    return ResponseModel(added_device, "Device added succesfully.")
