from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from models.device_schema import DeviceSchema
from models.response_schema import ResponseModel

from database.device_database import *

router = APIRouter()

@router.post("/", response_description="Device data added into the database")
async def add_device_router(device: DeviceSchema = Body(...)):
    added_device = await add_device(device)
    return ResponseModel(added_device, "Device added succesfully.")
