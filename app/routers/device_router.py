import imp
from fastapi import APIRouter

from app.services.device_service import DeviceService

router = APIRouter()
ds = DeviceService()

@router.get("/devices/")
async def get_all_devices():
    return ds.get_device()

