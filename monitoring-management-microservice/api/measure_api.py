from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from db.database_manager import DatabaseManager
from db.common import get_database
from models.error_schema import ErrorResponse
from models.measure_schema import Measure
from utils.logger import logger_config

logger = logger_config(__name__)

router = APIRouter(prefix="/measure")


@router.get(
    "s",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": List[Measure]},
        status.HTTP_406_NOT_ACCEPTABLE: {"model": ErrorResponse},
    },
)
async def get_all_measures_in_database(db: DatabaseManager = Depends(get_database)) -> List[Measure]:
    """
    Get all measures from measures mongodb collection
    """
    measures = await db.measure_get_all()
    if measures:
        return JSONResponse(status_code=status.HTTP_200_OK, content=measures)
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="database not ready"
    )


@router.get(
    "/{measure_id}",
    responses={
        status.HTTP_200_OK: {"model": Measure},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
)
async def get_measure_by_measure_id(measure_id: str, db: DatabaseManager = Depends(get_database)) -> Measure:
    """Get one measure by providing a measure_id: str"""
    measure = await db.measure_get_one(measure_id=measure_id)

    if measure:
        return JSONResponse(status_code=status.HTTP_200_OK, content=measure)

    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f"no measure found with measure_id: {measure_id}",
    )


@router.put(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": Measure},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
async def insert_a_new_measure(payload: Measure, db: DatabaseManager = Depends(get_database)) -> Measure:
    measure_created = await db.measure_insert_one(measure=payload)

    if measure_created:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=measure_created)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"measure could not be created",
    )


@router.patch(
    "",
    responses={
        status.HTTP_202_ACCEPTED: {"model": Measure},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
async def update_a_measure(payload: Measure, db: DatabaseManager = Depends(get_database)) -> Measure:
    measure_updated = await db.measure_update_one(measure=payload)

    if measure_updated:
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=measure_updated)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="measure could not be updated",
    )


@router.delete(
    "",
    responses={
        status.HTTP_202_ACCEPTED: {"model": Measure},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
async def delete_a_measure(payload: Measure, db: DatabaseManager = Depends(get_database)) -> List:
    measure_deleted = await db.measure_delete_one(measure=payload)

    if not measure_deleted:
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=[])

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"measure could not be deleted",
    )
