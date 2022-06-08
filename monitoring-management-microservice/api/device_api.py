from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from db.database_manager import DatabaseManager
from db.common import get_database
from models.error_schema import ErrorResponse
from models.device_schema import Device
from utils.logger import logger_config

from datetime import datetime
from uuid import uuid4

logger = logger_config(__name__)

router = APIRouter(prefix="/device")


@router.get(
    "s",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": List[Device]},
        status.HTTP_406_NOT_ACCEPTABLE: {"model": ErrorResponse},
    },
)
async def get_all_devices_in_database(db: DatabaseManager = Depends(get_database)) -> List[Device]:
    """
    Get all devices from devices mongodb collection
    """
    devices = await db.device_get_all()
    if devices:
        return JSONResponse(status_code=status.HTTP_200_OK, content=devices)
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Database not ready"
    )


@router.get(
    "/{device_id}",
    responses={
        status.HTTP_200_OK: {"model": Device},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
)
async def get_device_by_id(device_id: str, db: DatabaseManager = Depends(get_database)) -> Device:
    """
    Get one device by providing:
        - device_id: str
    """
    device = await db.device_get_one(device_id=device_id)

    if device:
        return JSONResponse(status_code=status.HTTP_200_OK, content=device)

    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f"No device is found with device_id: {device_id}",
    )


@router.put(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": Device},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
async def insert_a_new_device(measure: str, 
                              publish_qos: int, 
                              db: DatabaseManager = Depends(get_database)) -> Device:
    payload = Device.parse_obj({
        "device_id": str(uuid4()),
        "measure": measure,
        "publish_qos": publish_qos,
        "status": True,
        "update_datetime": datetime.utcnow().timestamp()
    })

    device_created = await db.device_insert_one(device=payload)

    if device_created:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=device_created)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"device could not be created",
    )


@router.patch(
    "",
    responses={
        status.HTTP_202_ACCEPTED: {"model": Device},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
async def update_a_device(device_id: str, 
                          measure: Optional[str], 
                          publish_qos: Optional[int],
                          status: bool,
                          db: DatabaseManager = Depends(get_database)) -> Device:
    
    payload = Device.parse_obj({
        "device_id": device_id,
        "measure": measure,
        "publish_qos": publish_qos,
        "status": status,
        "update_datetime": datetime.utcnow().timestamp()
    })

    device_updated = await db.device_update_one(device=payload)

    if device_updated:
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=device_updated)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="device could not be updated",
    )


@router.delete(
    "",
    responses={
        status.HTTP_202_ACCEPTED: {"model": Device},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
async def delete_a_device(
    payload: Device, db: DatabaseManager = Depends(get_database)
) -> list:
    device_deleted = await db.device_delete_one(device=payload)

    if not device_deleted:
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=[])

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"device could not be deleted",
    )
