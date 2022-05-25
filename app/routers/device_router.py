from fastapi import APIRouter

from typing import Optional

from services.device_service import *

router = APIRouter()

@router.post("/", response_description="Device data added into the database")
async def add_device(measure: str, publish_qos: int, decading_factor: Optional[float] = None):
    return await add_device(measure, publish_qos, decading_factor)
