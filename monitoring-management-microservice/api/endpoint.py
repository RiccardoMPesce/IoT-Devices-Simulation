import datetime

from fastapi import APIRouter

from api.device_api import router as device_router 
from api.measure_api import router as measure_router

endpoint = APIRouter(prefix="/")

endpoint.include_router(device_router)
endpoint.include_router(measure_router)

@endpoint.get("/", tags=["Root"], description="Root page, to show if the app is running or not")
def root():
    return {"status": "up", "timestamp": datetime.now()}