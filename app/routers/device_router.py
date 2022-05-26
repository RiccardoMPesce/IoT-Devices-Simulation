from fastapi import APIRouter, Body

from models.device_schema import DeviceSchema
from models.response_schema import ResponseModel

from services.device_service import *

router = APIRouter()

@router.post("/", response_description="Device data added into the database")
async def add_device_router(device: DeviceSchema = Body(...)):
    added_device = await add_device_service(device)
    return ResponseModel(added_device, "Device added succesfully.")
