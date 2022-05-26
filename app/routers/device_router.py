from fastapi import APIRouter

from typing import Optional, Union

from services.device_service import *

router = APIRouter()

@router.post("/", response_description="Device data added into the database")
async def add_device(measure: str, publish_qos: int, status: Union[bool, int, str, None], decading_factor: Optional[float] = None):
    return await add_device(measure, publish_qos, status, decading_factor)
