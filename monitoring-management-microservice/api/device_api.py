from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from db.database_manager import DeviceDatabaseManager
from db.common import get_device_database
from models.error_schema import ErrorResponse
from models.device_schema import Device
from utils.logger import logger_config

logger = logger_config(__name__)

router = APIRouter(prefix="/device")


@router.get(
    "all",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": List[Device]},
        status.HTTP_406_NOT_ACCEPTABLE: {"model": ErrorResponse},
    },
)
async def get_all_devices_in_database(db: DeviceDatabaseManager = Depends(get_device_database)) -> List[Device]:
    """
    Get all devices from devices mongodb collection
    """
    users = await db.user_get_all()
    if users:
        return JSONResponse(status_code=status.HTTP_200_OK, content=users)
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="database not ready"
    )


@router.get(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": Device},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
)
async def get_user_by_user_id(
    user_id: str, db: DeviceDatabaseManager = Depends(get_device_database)
) -> Device:
    """Get one user by providing a user_id: str"""
    user = await db.user_get_one(user_id=user_id)

    if user:
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)

    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f"no user found with user_id: {user_id}",
    )


@router.put(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": Device},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
async def insert_a_new_user(
    payload: Device, db: DeviceDatabaseManager = Depends(get_device_database)
) -> Device:
    user_created = await db.user_insert_one(user=payload)

    if user_created:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=user_created)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"user could not be created",
    )


@router.patch(
    "",
    responses={
        status.HTTP_202_ACCEPTED: {"model": Device},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
async def update_a_user(
    payload: Device, db: DeviceDatabaseManager = Depends(get_device_database)
) -> Device:
    user_updated = await db.user_update_one(user=payload)

    if user_updated:
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=user_updated)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="user could not be updated",
    )


@router.delete(
    "",
    responses={
        status.HTTP_202_ACCEPTED: {"model": Device},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
async def delete_a_user(
    payload: Device, db: DeviceDatabaseManager = Depends(get_device_database)
) -> list:
    user_deleted = await db.user_delete_one(user=payload)

    if not user_deleted:
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=[])

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"user could not be deleted",
    )
