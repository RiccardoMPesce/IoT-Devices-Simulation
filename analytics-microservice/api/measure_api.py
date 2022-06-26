from fastapi import APIRouter

from db.database import stats_by_measure, last_measure_state


router = APIRouter(prefix="/measure")


@router.get("/stats/{measure}", description="Get stats by measure")
async def get_stats_by_measure(measure: str):
    result = await stats_by_measure(measure)
    return result

@router.get("/last_state/{measure}", description="Get last state by measure")
async def get_stats_by_measure(measure: str):
    result = await last_measure_state(measure)
    return result
