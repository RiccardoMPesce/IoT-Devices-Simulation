from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from pydantic import Field
from typing import Union
from datetime import datetime

from db.common import get_database, DatabaseManager

from device_api import router as device_router

from utils.logger import logger_config


router = APIRouter(prefix="/simulate")

@router.put(
    "/{device_id}/{measure_value}",
    responses={
        status.HTTP_201_CREATED,
        status.HTTP_404_NOT_FOUND,
    },
)
async def simulate_recording(device_id: str, 
                             measure_value: Union[int, bool, float, str], 
                             health: str = Field(["good", "bad", "ko"]), 
                             db: DatabaseManager = Depends(get_database)) -> list:
    device = await db.device_get_one({"device_id": device_id})

    if device:
        measure = {
            "device_id": device_id,
            "measure": device.get("measure"),
            "measure_value": measure_value,
            "health": health,
            "timestamp": datetime.utcnow().timestamp()
        }
    else:
        return JSONResponse([], status_code=status.HTTP_404_NOT_FOUND)

