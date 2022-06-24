from datetime import datetime
from fastapi import APIRouter, status
from typing import List
from fastapi.exceptions import HTTPException

from db.database import Record

endpoint = APIRouter()

@endpoint.get("/", tags=["Root"], description="Root page, to show if the app is running or not")
def root():
    return {"status": "up", "timestamp": datetime.now()}


@endpoint.get("/all", response_model=List[Record])
async def get_all_recordings():
    try:
        records = await Record.objects.all()
        return records 
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch records")


@endpoint.get("/{device_id}", response_model=List[dict])
async def get_recordings_by_id(device_id: str):
    try:
        records = await Record.objects.all(device_id=device_id)
        return records 
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Failed to fetch records for device {device_id}"
        )


@endpoint.get("/{measure}", response_model=List[dict])
async def get_recordings_by_id(measure: str):
    try:
        records = await Record.objects.all(measure=measure)
        return records 
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Failed to fetch records for measure {measure}"
        )