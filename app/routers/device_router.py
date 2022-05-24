from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from repository.device_database import add_device, delete_device, retrieve_device, retrieve_devices, update_device
from models.device_schema import DeviceSchema, UpdateDeviceModel

router = APIRouter()

@router.post("/", response_description="Device data added into the database")
async def add_student_data(device: DeviceSchema = Body(...)):
    device = jsonable_encoder(device)
    new_device = await add_device(device)
    return {"Added": str(bool(new_device))}
