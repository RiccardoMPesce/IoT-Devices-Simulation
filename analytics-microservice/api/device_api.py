from fastapi import APIRouter

from db.database import stats_by_device, last_device_state


router = APIRouter(prefix="/device")


@router.get("/stats/{device_id}", description="Get stats by device_id")
async def get_stats_by_device_id(device_id: str):
    result = await stats_by_device(device_id)
    return result

@router.get("/last_state/{device_id}", description="Get last state by device_id")
async def get_stats_by_device_id(device_id: str):
    result = await last_device_state(device_id)
    return result
    