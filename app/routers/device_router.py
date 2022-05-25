from fastapi import APIRouter

from typing import Optional

from models.device_schema import DeviceSchema, UpdateDeviceModel
from services.device_service import DeviceService

router = APIRouter()
device_service = DeviceService()

@router.post("/", response_description="Device data added into the database")
async def add_device(measure: str, publish_qos: int, decading_factor: Optional[float] = None):
    return await device_service.add_device(measure, publish_qos, decading_factor)
